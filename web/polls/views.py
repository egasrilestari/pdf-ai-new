from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .utils import *
from concurrent.futures import ThreadPoolExecutor
from django.http import FileResponse
from django.conf import settings
from PIL import Image
from django.forms.models import model_to_dict
from docx import Document
from pathlib import Path
from PyPDF2 import PdfMerger

import tempfile
import smtplib
import os
import pandas as pd
import numpy as np
import traceback
import datetime
import pytz
import io
import base64
import uuid
import bcrypt
import logging
import requests
import glob

date = pytz.timezone("Asia/Jakarta")
date = datetime.datetime.now(date)
created_at_column = date.strftime("%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("django.request")
logger.info("The info message")
logger.warning("The warning message")
logger.error("The error message")


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    context = {}
    user_name = request.session.get("user_name")
    user_type = request.session.get("user_type")
    user_type = int(user_type)

    if user_name:
        context["name"] = user_name
        context["type"] = user_type

    return render(request, "index.html", context)


def login(request):
    context = {}
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = Users.objects.filter(email=email).first()

            if not user:
                context["error"] = "Email tidak ditemukan"
                logger.error("Email tidak ditemukan")
            else:
                hashed = user.password.encode("utf-8")  # ambil hash dari db
                password_bytes = password.encode("utf-8")  # password input user

                if bcrypt.checkpw(password_bytes, hashed):
                    # simpen name di session
                    request.session["user_name"] = user.name
                    request.session["user_id"] = user.id
                    request.session["user_email"] = user.email
                    request.session["user_type"] = user.type
                    # Password benar
                    logger.debug("Success login")
                    return redirect("index")
                else:
                    context["error"] = "Password salah"
                    logger.error("Password salah")
    except Exception as e:
        print("Error login function:", e)
        context["error"] = "Terjadi kesalahan saat login"
        logger.error("Terjadi kesalahan saat login")

    return render(request, "login.html", context)


def logout(request):
    request.session.flush()  # Hapus semua session
    return redirect("login")


# function merge all pdf
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path ke folder /polls/
PDF_DIR = os.path.join(BASE_DIR, "files", "pdf")  # path ke /polls/files/pdf/


def merge_all_pdfs():
    pattern = os.path.join(PDF_DIR, "*.pdf")
    all_pdf_files = glob.glob(pattern)

    if not all_pdf_files:
        return None, None

    merger = PdfMerger()
    for pdf_file in all_pdf_files:
        merger.append(pdf_file)

    pdf_buffer = io.BytesIO()
    merger.write(pdf_buffer)
    merger.close()
    pdf_buffer.seek(0)

    return pdf_buffer, "gabungan_semua_file.pdf"


def merge_all_docxs():
    pattern = os.path.join(PDF_DIR, "*.docx")
    all_docx_files = glob.glob(pattern)

    if not all_docx_files:
        return None, None

    merged_text = ""

    for docx_file in all_docx_files:
        document = Document(docx_file)
        file_text = "\n".join(
            [para.text for para in document.paragraphs if para.text.strip() != ""]
        )
        merged_text += f"\n\n==== {os.path.basename(docx_file)} ====\n\n{file_text}"

    return merged_text, "gabungan_semua_file.txt"


def readfile_to_n8n(request):
    context = {}
    user_name = request.session.get("user_name")
    context["name"] = user_name

    file_history = request.session.get("file_history", [])

    try:
        if request.method == "POST":
            user_input = request.POST.get("message", "")
            file = request.FILES.get("formFile", None)

            summary = None
            file_name = None

            # === Jika ada file diupload ===
            if file:
                file_name = file.name
                files = {"formFile": (file.name, file.read(), file.content_type)}
                response = requests.post(
                    "https://discrete-quail-monthly.ngrok-free.app/webhook/from-python",
                    files=files,
                )
                try:
                    summary = response.json().get(
                        "result", "Tidak ada ringkasan ditemukan."
                    )
                except:
                    summary = "Gagal mendapatkan respon dari n8n."

                file_history.append(
                    {"role": "user", "message": f"Mengunggah file: {file_name}"}
                )
                file_history.append(
                    {
                        "role": "ai",
                        "file_name": file_name,
                        "summary": summary,
                    }
                )

            elif user_input.strip().lower().startswith("ringkas file"):
                try:
                    print("masuk ke elif ringkas file")
                    parts = user_input.strip().split(
                        " ", 2
                    )  # "ringkas file data pipeline"

                    if len(parts) >= 3:
                        # Step 1: Ambil nama file mentah
                        raw_file_name = parts[2].strip()
                        search_file_name = raw_file_name.replace(" ", "_").lower()

                        # Step 2: Cari file PDF yang namanya cocok sebagian
                        pattern = os.path.join(PDF_DIR, f"*{search_file_name}*.pdf")
                        matching_files = glob.glob(pattern)

                        if matching_files:
                            merger = PdfMerger()
                            for pdf_file in matching_files:
                                merger.append(pdf_file)

                            # Step 3: Simpan jadi satu PDF baru (bisa juga ke memory nanti)
                            output_pdf_path = os.path.join(PDF_DIR, "merged_output.pdf")
                            with open(output_pdf_path, "wb") as f_out:
                                merger.write(f_out)
                            merger.close()

                            # Step 4: Kirim PDF gabungan ke webhook
                            with open(output_pdf_path, "rb") as f:
                                file_content = f.read()

                            files = {
                                "formFile": (
                                    "merged_output.pdf",
                                    file_content,
                                    "application/pdf",
                                ),
                            }

                            response = requests.post(
                                "https://discrete-quail-monthly.ngrok-free.app/webhook/from-python",
                                files=files,
                            )

                            try:
                                summary = response.json().get(
                                    "result", "Tidak ada ringkasan ditemukan."
                                )
                            except:
                                summary = "Gagal mendapatkan respon dari n8n."

                            file_history.append({"role": "user", "message": user_input})
                            file_history.append(
                                {
                                    "role": "ai",
                                    "file_name": output_pdf_path,
                                    "summary": summary,
                                }
                            )

                        else:
                            summary = f"Tidak ditemukan file PDF dengan nama mengandung `{search_file_name}` di /polls/files/pdf/."
                            file_history.append({"role": "user", "message": user_input})
                            file_history.append({"role": "ai", "summary": summary})

                    else:
                        summary = (
                            "Format perintah salah. Contoh: Ringkas file data pipeline"
                        )
                        file_history.append({"role": "user", "message": user_input})
                        file_history.append({"role": "ai", "summary": summary})

                except Exception as e:
                    summary = f"Terjadi kesalahan: {str(e)}"
                    file_history.append({"role": "user", "message": user_input})
                    file_history.append({"role": "ai", "summary": summary})
            # === Jika hanya kirim pesan teks (misal pertanyaan tentang file) ===
            elif user_input.strip():
                merged_pdf_buffer, merged_pdf_name = merge_all_pdfs()
                # === aktifin read file docx ===
                # merged_text, merged_docx_name = merge_all_docxs()
                payload = {"input": user_input}
                # "merged_docx_text": merged_text or ""

                files = {}
                if merged_pdf_buffer:
                    files["formFile"] = (
                        merged_pdf_name,
                        merged_pdf_buffer,
                        "application/pdf",
                    )
                else:
                    files = None
                    print("Tidak ada file PDF untuk dikirim.")

                response = requests.post(
                    "https://discrete-quail-monthly.ngrok-free.app/webhook/from-python",
                    data=payload,
                    files=files if files else None,
                )
                try:
                    summary = response.json().get("result", "Tidak ada respon.")
                except:
                    summary = "Gagal mendapatkan respon dari n8n."

                file_history.append({"role": "user", "message": user_input})
                file_history.append({"role": "ai", "summary": summary})

            # Simpan ke session
            request.session["file_history"] = file_history

    except Exception as e:
        print("❌ Error:", str(e))
        traceback.print_exc()

    context["file_history"] = request.session.get("file_history", [])
    return render(request, "read_file.html", context)
