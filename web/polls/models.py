from django.db import models


class Events(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_code = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    descp = models.TextField()
    banner_img = models.TextField()
    banner_descp = models.CharField(max_length=100)
    from_field = models.DateTimeField(
        db_column="from"
    )  # Field renamed because it was a Python reserved word.
    to = models.DateTimeField()
    venue = models.CharField(max_length=100)
    gmaps = models.TextField()
    event_type = models.IntegerField(db_comment="ditambahin master data event_type")
    floorplan = models.CharField(max_length=50)
    header_tiket = models.CharField(max_length=255)
    status = models.IntegerField(db_comment="event ditampilin apa engga")
    start_sale_date = models.DateTimeField()
    end_sale_date = models.DateTimeField()
    slug = models.CharField(max_length=255, blank=True, null=True)
    promo = models.IntegerField()
    api_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    layout_tix = models.CharField(max_length=500, blank=True, null=True)
    onsite = models.IntegerField(
        blank=True, null=True, db_comment="untuk dibuka di os.dyandratiket"
    )
    detail_penukaran = models.TextField(
        blank=True, null=True, db_comment="lokasi penukaran, jdwal dll"
    )
    is_admin_fee = models.IntegerField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "events"

    def __str__(self):
        return (
            self.id,
            self.event_code,
            self.name,
            self.descp,
            self.banner_img,
            self.banner_descp,
            self.from_field,
            self.to,
            self.venue,
            self.gmaps,
            self.event_type,
            self.floorplan,
            self.header_tiket,
            self.status,
            self.start_sale_date,
            self.end_sale_date,
            self.slug,
            self.promo,
            self.api_id,
            self.created_at,
            self.updated_at,
            self.layout_tix,
            self.onsite,
            self.detail_penukaran,
            self.is_admin_fee,
            self.link,
        )


class Orderapi(models.Model):
    id = models.BigAutoField(primary_key=True)
    # event_id = models.IntegerField(blank=True, null=True)
    event_id = models.ForeignKey("Events", models.DO_NOTHING, db_column="event_id")
    # user_id = models.IntegerField(blank=True, null=True)
    user_id = models.ForeignKey("Users", models.DO_NOTHING, db_column="user_id")
    agent_id = models.IntegerField(blank=True, null=True)
    promo_id = models.IntegerField(blank=True, null=True)
    booking_code = models.CharField(unique=True, max_length=255, blank=True, null=True)
    category_type = models.CharField(max_length=255, blank=True, null=True)
    name_category = models.CharField(max_length=255, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    name = models.CharField(
        max_length=255, db_collation="utf8mb4_unicode_ci", blank=True, null=True
    )
    name_last = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    ktp = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    api_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    api_invoice_code = models.CharField(max_length=255, blank=True, null=True)
    api_order_id = models.CharField(max_length=255, blank=True, null=True)
    api_quantity_total = models.IntegerField(blank=True, null=True)
    api_payment_total = models.IntegerField(blank=True, null=True)
    token_api = models.CharField(max_length=255, blank=True, null=True)
    api_status_order = models.CharField(max_length=255, blank=True, null=True)
    api_attendees_id = models.IntegerField(blank=True, null=True)
    api_evoucher = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    type = models.IntegerField()
    is_paid = models.IntegerField()
    is_manual = models.IntegerField(blank=True, null=True)
    reff = models.CharField(max_length=255, blank=True, null=True)
    approval_id = models.IntegerField(blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    onsite = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "orderapi"

    def __str__(self):
        return (
            self.id,
            self.event_id,
            self.user_id,
            self.agent_id,
            self.promo_id,
            self.booking_code,
            self.category_type,
            self.name_category,
            self.qty,
            self.price,
            self.fee,
            self.discount,
            self.total,
            self.name,
            self.name_last,
            self.email,
            self.phone,
            self.ktp,
            self.payment_type,
            self.api_invoice_id,
            self.api_invoice_code,
            self.api_order_id,
            self.api_quantity_total,
            self.api_payment_total,
            self.token_api,
            self.api_status_order,
            self.api_attendees_id,
            self.api_evoucher,
            self.created_at,
            self.updated_at,
            self.status,
            self.type,
            self.is_paid,
            self.is_manual,
            self.reff,
            self.approval_id,
            self.approval_date,
            self.onsite,
        )


class ScanLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    # qrcode = models.CharField(max_length=255, blank=True, null=True)
    qrcode = models.ForeignKey(
        "Orderapidt", models.DO_NOTHING, db_column="qrcode", to_field="barcode"
    )
    scan_in = models.CharField(max_length=255, blank=True, null=True)
    scan_out = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    specify = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    # event_id = models.PositiveBigIntegerField(blank=True, null=True)
    event = models.ForeignKey(
        "Events", models.DO_NOTHING, db_column="event_id", to_field="id"
    )
    gate = models.CharField(max_length=255, blank=True, null=True)
    gate_out = models.CharField(max_length=255, blank=True, null=True)
    top_up = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "scan_logs"

    def __str__(self):
        return (
            self.id,
            self.qrcode,
            self.scan_in,
            self.scan_out,
            self.created_at,
            self.updated_at,
            self.category,
            self.specify,
            self.user_id,
            self.event_id,
            self.gate,
            self.gate_out,
            self.top_up,
        )


class QueryLogs(models.Model):
    query = models.TextField(blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    logs = models.CharField(max_length=255, blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    correct_sql = models.TextField(blank=True, null=True)
    is_used_for_training = models.BooleanField(default=False)
    user = models.ForeignKey("Users", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "query_logs"

    def __str__(self):
        return (
            self.query,
            self.keyword,
            self.logs,
            self.error,
            self.updated_at,
            self.created_at,
            self.result,
            self.correct_sql,
            self.is_used_for_training,
            self.user,
        )


class ReportLogs(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True)
    report_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    chart_config = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "report_logs"

    def __str__(self):
        return (
            self.uuid,
            self.report_name,
            self.created_at,
            self.updated_at,
            self.chart_config,
        )


class Orderapidt(models.Model):
    id = models.BigAutoField(primary_key=True)
    # order_id = models.IntegerField()
    order = models.ForeignKey(
        "Orderapi", on_delete=models.CASCADE, db_column="order_id"
    )
    # code = models.IntegerField()
    code = models.ForeignKey("Cateprice", models.DO_NOTHING, db_column="code")
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    ktp = models.CharField(max_length=255, blank=True, null=True)
    domisili = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    qty = models.IntegerField(db_comment="ga dipake")
    discount = models.IntegerField(blank=True, null=True)
    total = models.IntegerField()
    barcode = models.CharField(max_length=255, blank=True, null=True, unique=True)
    flag = models.IntegerField(db_comment="ga dipake")
    scanin = models.IntegerField(blank=True, null=True)
    scanout = models.IntegerField()
    loc = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ga dipake"
    )
    view = models.IntegerField(blank=True, null=True, db_comment="udah brp kali diliat")
    print = models.IntegerField(db_comment="sudah di print brapa kali")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    is_take = models.IntegerField(blank=True, null=True)
    claim_by = models.CharField(max_length=255, blank=True, null=True)
    take_date = models.DateTimeField(blank=True, null=True)
    take_from = models.IntegerField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    nation = models.CharField(max_length=255, blank=True, null=True)
    salutation = models.CharField(max_length=255, blank=True, null=True)
    bulk_input = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    day1 = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    day2 = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    day3 = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    seat_no = models.IntegerField(blank=True, null=True)
    table = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    kit = models.IntegerField(blank=True, null=True, db_comment="ga dipake")

    class Meta:
        managed = False
        db_table = "orderapidt"

    def __str__(self):
        return (
            self.id,
            self.order,
            self.code,
            self.name,
            self.price,
            self.ktp,
            self.domisili,
            self.phone,
            self.qty,
            self.discount,
            self.total,
            self.barcode,
            self.flag,
            self.scanin,
            self.scanout,
            self.loc,
            self.view,
            self.print,
            self.created_at,
            self.updated_at,
            self.user_id,
            self.is_take,
            self.claim_by,
            self.take_date,
            self.take_from,
            self.company,
            self.nation,
            self.salutation,
            self.bulk_input,
            self.day1,
            self.day2,
            self.day3,
            self.seat_no,
            self.table,
            self.kit,
        )


class Cateprice(models.Model):
    id = models.BigAutoField(primary_key=True)
    prefix = models.CharField(
        max_length=255, blank=True, null=True, db_comment="kode category tiket"
    )
    name_category = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    id_event = models.IntegerField()
    value_normal = models.IntegerField()
    value_usd = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    value_employee = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    in_stock = models.IntegerField(blank=True, null=True)
    track_stock = models.IntegerField(blank=True, null=True)
    value_agent = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    stock_normal = models.IntegerField(db_comment="ga dipake")
    stock_employee = models.IntegerField(db_comment="ga dipake")
    stock_agent = models.IntegerField(db_comment="ga dipake")
    discount_amt = models.IntegerField(db_comment="ga dipake")
    discount_pct = models.IntegerField(db_comment="ga dipake")
    tax_pct = models.IntegerField(db_comment="ga dipake")
    status = models.IntegerField()
    stock_global = models.IntegerField(db_comment="ga dipake")
    multiply = models.IntegerField()
    multiply_val = models.IntegerField(blank=True, null=True)
    live_stream = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    link_live = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ga dipake"
    )
    promo = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    invitation = models.IntegerField()
    is_idcard = models.IntegerField(blank=True, null=True)
    special = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    is_topup = models.IntegerField(blank=True, null=True)
    sale_nw = models.IntegerField()
    bg = models.CharField(max_length=255, blank=True, null=True)
    style_view = models.TextField(blank=True, null=True)
    style_pdf = models.TextField(blank=True, null=True)
    tnc = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ga dipake"
    )
    api_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    venue = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ga dipake"
    )
    limit = models.IntegerField(blank=True, null=True)
    bundling = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    premium = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    premium_date = models.DateField(blank=True, null=True, db_comment="ga dipake")
    orientation = models.CharField(
        max_length=255, blank=True, null=True, db_comment="layout tiket"
    )
    papper = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    is_seating = models.IntegerField(blank=True, null=True)
    xplorin_id = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ga dipake"
    )
    zone = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ga dipake"
    )
    cat = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ga dipake"
    )
    sort = models.IntegerField(blank=True, null=True)
    poster = models.CharField(max_length=255, blank=True, null=True)
    is_show_partner = models.IntegerField()
    is_date_chose = models.IntegerField(db_comment="ganti ke start date")
    date_chose = models.CharField(
        max_length=255, blank=True, null=True, db_comment="ganti ke end date"
    )
    onsite = models.IntegerField(blank=True, null=True)
    is_custome_qr = models.IntegerField(blank=True, null=True)
    custome_qr_width = models.DecimalField(
        max_digits=10, decimal_places=1, blank=True, null=True
    )
    custome_qr_height = models.DecimalField(
        max_digits=10, decimal_places=1, blank=True, null=True
    )
    is_sold_out = models.IntegerField()
    show_dashtix = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cateprice"

    def __str__(self):
        return (
            self.id,
            self.prefix,
            self.max_length,
            self.name_category,
            self.description,
            self.id_event,
            self.value_normal,
            self.value_usd,
            self.value_employee,
            self.in_stock,
            self.track_stock,
            self.value_agent,
            self.stock_normal,
            self.stock_employee,
            self.stock_agent,
            self.discount_amt,
            self.discount_pct,
            self.tax_pct,
            self.status,
            self.stock_global,
            self.multiply,
            self.multiply_val,
            self.live_stream,
            self.link_live,
            self.max_length,
            self.promo,
            self.invitation,
            self.is_idcard,
            self.special,
            self.is_topup,
            self.sale_nw,
            self.bg,
            self.style_view,
            self.style_pdf,
            self.tnc,
            self.max_length,
            self.api_id,
            self.created_at,
            self.updated_at,
            self.venue,
            self.max_length,
            self.limit,
            self.bundling,
            self.premium,
            self.premium_date,
            self.orientation,
            self.max_length,
            self.papper,
            self.is_group,
            self.group_id,
            self.is_seating,
            self.xplorin_id,
            self.max_length,
            self.zone,
            self.max_length,
            self.cat,
            self.max_length,
            self.sort,
            self.poster,
            self.is_show_partner,
            self.is_date_chose,
            self.date_chose,
            self.max_length,
            self.onsite,
            self.is_custome_qr,
            self.custome_qr_width,
            self.max_digits,
            self.custome_qr_height,
            self.max_digits,
            self.is_sold_out,
            self.show_dashtix,
        )


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    two_factor_secret = models.TextField(blank=True, null=True)
    two_factor_recovery_codes = models.TextField(blank=True, null=True)
    two_factor_confirmed_at = models.DateTimeField(blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    current_team_id = models.PositiveBigIntegerField(blank=True, null=True)
    profile_photo_path = models.CharField(max_length=2048, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(db_comment="1=user,2=admin,3=agent")
    mobile_phone = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    id_nation = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.CharField(max_length=255, blank=True, null=True)
    admin = models.IntegerField(blank=True, null=True)
    event = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    event_id = models.IntegerField(blank=True, null=True, db_comment="ga dipake")
    kompas = models.IntegerField()
    location_id = models.IntegerField(blank=True, null=True)
    password_resets = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    reff = models.CharField(max_length=255, blank=True, null=True)
    saf = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return (
            self.id,
            self.name,
            self.email,
            self.email_verified_at,
            self.password,
            self.two_factor_secret,
            self.two_factor_recovery_codes,
            self.two_factor_confirmed_at,
            self.remember_token,
            self.current_team_id,
            self.profile_photo_path,
            self.created_at,
            self.updated_at,
            self.type,
            self.mobile_phone,
            self.gender,
            self.address,
            self.city,
            self.country,
            self.id_nation,
            self.birth_date,
            self.admin,
            self.event,
            self.event_id,
            self.kompas,
            self.location_id,
            self.password_resets,
            self.age,
            self.reff,
            self.saf,
        )


class Acronyms(models.Model):
    acronym = models.CharField(max_length=255, blank=True, null=True)
    meaning = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "acronyms"

    def __str__(self):
        return (self.acronym, self.meaning)
