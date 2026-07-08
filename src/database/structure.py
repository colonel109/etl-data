import datetime
from typing import Optional, List
from sqlalchemy import (
    String, Text, Date, Boolean, DateTime,
    ForeignKey, CheckConstraint, UniqueConstraint, Index, Numeric, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# Bảng transactions staging
class TransactionsStaging(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    added_date: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
        )
    
    business_partner_code: Mapped[str | None] = mapped_column(String())
    business_partner_name: Mapped[str | None] = mapped_column(String())
    team_name: Mapped[str | None] = mapped_column(String())
    branch_name: Mapped[str | None] = mapped_column(String())
    bp_group_name: Mapped[str | None] = mapped_column(String())
    product_code: Mapped[str | None] = mapped_column(String())
    product_name: Mapped[str | None] = mapped_column(String())
    source_product_code: Mapped[str | None] = mapped_column(String())
    source_product_name: Mapped[str | None] = mapped_column(String())
    document_type_name: Mapped[str | None] = mapped_column(String())
    sell_type_name: Mapped[str | None] = mapped_column(String())
    cost_center_code: Mapped[str | None] = mapped_column(String())
    cost_center_name: Mapped[str | None] = mapped_column(String())
    profit_center_code: Mapped[str | None] = mapped_column(String())
    profit_center_name: Mapped[str | None] = mapped_column(String())
    warehouse_code: Mapped[str | None] = mapped_column(String())
    warehouse_name: Mapped[str | None] = mapped_column(String())
    return_type_code: Mapped[str | None] = mapped_column(String())
    return_type_name: Mapped[str | None] = mapped_column(String())
    uom_name: Mapped[str | None] = mapped_column(String())
    document_no: Mapped[str | None] = mapped_column(String())
    tax_code: Mapped[str | None] = mapped_column(String())
    tax_number: Mapped[str | None] = mapped_column(String())
    
    posting_date: Mapped[datetime.date | None] = mapped_column(Date)
    due_date: Mapped[datetime.date | None] = mapped_column(Date)
    demand_date: Mapped[datetime.date | None] = mapped_column(Date)
    final_delivery_date: Mapped[datetime.date | None] = mapped_column(Date)
    
    weight: Mapped[float | None] = mapped_column(Numeric())
    uom_per_quantity: Mapped[float | None] = mapped_column(Numeric())
    uom_quantity: Mapped[float | None] = mapped_column(Numeric())
    quantity: Mapped[float | None] = mapped_column(Numeric())
    quantity_packaging_uom: Mapped[float | None] = mapped_column(Numeric())
    box: Mapped[float | None] = mapped_column(Numeric())
    base_price: Mapped[float | None] = mapped_column(Numeric())
    discount_percent: Mapped[float | None] = mapped_column(Numeric())
    discounted_price: Mapped[float | None] = mapped_column(Numeric())
    discounted_price_tax: Mapped[float | None] = mapped_column(Numeric())
    sales_revenue: Mapped[float | None] = mapped_column(Numeric())
    sales_amount_fc: Mapped[float | None] = mapped_column(Numeric())
    tax_amount: Mapped[float | None] = mapped_column(Numeric())
    tax_amount_fc: Mapped[float | None] = mapped_column(Numeric())
    sales_amount_tax: Mapped[float | None] = mapped_column(Numeric())
    sales_amount_fc_tax: Mapped[float | None] = mapped_column(Numeric())
    return_quantity: Mapped[float | None] = mapped_column(Numeric())
    remark: Mapped[str | None] = mapped_column(String())


class Dept(Base):
    __tablename__ = "dept"
    __table_args__ = {"schema": "main"}

    dept_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dept_name: Mapped[str] = mapped_column(String())

    teams: Mapped[list["Team"]] = relationship(back_populates="dept")


class Channel(Base):
    __tablename__ = "channel"
    __table_args__ = {"schema": "main"}

    channel_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_name: Mapped[str] = mapped_column(String())

    branches: Mapped[list["Branch"]] = relationship(back_populates="channel")


class Branch(Base):
    __tablename__ = "branch"
    __table_args__ = {"schema": "main"}

    branch_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    branch_name: Mapped[str] = mapped_column(String())
    dept_key: Mapped[str] = mapped_column(ForeignKey("main.dept.dept_key"))
    channel_key: Mapped[int] = mapped_column(ForeignKey("main.channel.channel_key"))

    channel: Mapped["Channel"] = relationship(back_populates="branches")
    teams: Mapped[list["Team"]] = relationship(back_populates="branch")


class Team(Base):
    __tablename__ = "team"
    __table_args__ = {"schema": "main"}

    team_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_name: Mapped[str] = mapped_column(String())
    branch_key: Mapped[int] = mapped_column(ForeignKey("main.branch.branch_key"))

    branch: Mapped["Branch"] = relationship(back_populates="teams") 


class KpiGroup(Base):
    __tablename__ = "kpi_group"
    __table_args__ = {"schema": "main"}

    kpi_group_key: Mapped[int] = mapped_column(primary_key=True)
    sub_kpi_1: Mapped[Optional[str]] = mapped_column(String())
    sub_kpi_2: Mapped[Optional[str]] = mapped_column(String())
    sub_kpi_3: Mapped[Optional[str]] = mapped_column(String())
    sub_kpi_0: Mapped[Optional[str]] = mapped_column(String())

    product_categories: Mapped[list["ProductCategory"]] = relationship(back_populates="kpi_group")


class Market(Base):
    __tablename__ = "market"
    __table_args__ = {"schema": "main"}

    market_key: Mapped[int] = mapped_column(primary_key=True)
    market_type_name: Mapped[str] = mapped_column(String())
    country_name_eng: Mapped[str] = mapped_column(String())
    country_shortname_a2: Mapped[str] = mapped_column(String())
    country_name_vi: Mapped[Optional[str]] = mapped_column(String())

    products: Mapped[list["Product"]] = relationship(back_populates="market")


class ProductCategory(Base):
    __tablename__ = "product_category"
    __table_args__ = {"schema": "main"}

    product_category_key: Mapped[int] = mapped_column(primary_key=True)
    product_category_name: Mapped[Optional[str]] = mapped_column(String())
    kpi_group_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.kpi_group.kpi_group_key"))

    kpi_group: Mapped[Optional["KpiGroup"]] = relationship(back_populates="product_categories")
    products: Mapped[list["Product"]] = relationship(back_populates="product_category")


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "main"}

    product_key: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column()
    product_name: Mapped[Optional[str]] = mapped_column(String())
    product_category_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.product_category.product_category_key"))
    market_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.market.market_key"), server_default="0")
    msg_group_key: Mapped[Optional[int]] = mapped_column()
    product_spec: Mapped[Optional[int]] = mapped_column()
    product_name_eng: Mapped[Optional[str]] = mapped_column()
    ducviet_category_key: Mapped[Optional[int]] = mapped_column()

    product_category: Mapped[Optional["ProductCategory"]] = relationship(back_populates="products")
    market: Mapped[Optional["Market"]] = relationship(back_populates="products")


class Warehouse(Base):
    __tablename__ = "warehouse"
    __table_args__ = {"schema": "main"}

    warehouse_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    warehouse_code: Mapped[int] = mapped_column(String(), unique=True)
    warehouse_name: Mapped[int] = mapped_column(String())


class Province(Base):
    __tablename__ = "province"
    __table_args__ = {"schema": "main"}

    province_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    province_name_old: Mapped[str] = mapped_column(String(), unique=True)
    province_name_new: Mapped[str] = mapped_column(String())


class BusinessPartnerType(Base):
    __tablename__ = "business_partner_type"
    __table_args__ = {"schema": "main"}

    bp_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bp_type_name: Mapped[Optional[str]] = mapped_column(String())

    # 1 Type có NHIỀU Group (Dùng List)
    groups: Mapped[List["BusinessPartnerGroup"]] = relationship(
        back_populates="partner_type"
    )


class BusinessPartnerGroup(Base):
    __tablename__ = "business_partner_group"
    __table_args__ = {"schema": "main"}

    bp_group_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bp_group_name: Mapped[Optional[str]] = mapped_column(String())
    
    bp_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.business_partner_type.bp_type_key")
    )

    partner_type: Mapped[Optional["BusinessPartnerType"]] = relationship(
        back_populates="groups"
    )

    partners: Mapped[List["BusinessPartner"]] = relationship(
        back_populates="partner_group"
    )


class BusinessPartner(Base):
    __tablename__ = "business_partner"
    __table_args__ = (
        UniqueConstraint("business_partner_code", "valid_from", name="unique_bp_key_valid_from"),
        CheckConstraint(
            "((is_current = true AND valid_to IS NULL) OR (is_current = false))",
            name="is_current_valid"
        ),
        Index("idx_bp_code_period", "business_partner_code", "valid_from", "valid_to"),
        {"schema": "main"}
    )

    business_partner_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    business_partner_code: Mapped[str] = mapped_column(Text)
    business_partner_name: Mapped[Optional[str]] = mapped_column(String())
    
    creation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    import_date: Mapped[Optional[datetime.date]] = mapped_column(
        Date, server_default=func.current_date()
    )
    
    bp_group_key: Mapped[Optional[int]] = mapped_column(
        ForeignKey("main.business_partner_group.bp_group_key")
    )
    team_key: Mapped[Optional[int]] = mapped_column(
        ForeignKey("main.team.team_key")
    )
    province_key: Mapped[Optional[int]] = mapped_column(
        ForeignKey("main.province.province_key")
    )
    
    temporary_bp_key: Mapped[Optional[bool]] = mapped_column(Boolean, server_default="false")
    
    valid_from: Mapped[Optional[datetime.date]] = mapped_column(
        Date, server_default=func.date_trunc("month", func.now())
    )
    valid_to: Mapped[Optional[datetime.date]] = mapped_column(Date)
    is_current: Mapped[Optional[bool]] = mapped_column(Boolean, server_default="true")

    partner_group: Mapped[Optional["BusinessPartnerGroup"]] = relationship(
        back_populates="partners"
    )

class DocumentType(Base):
    __tablename__ = "document_type"
    __table_args__ = {"schema": "main"}

    document_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_type_code: Mapped[str] = mapped_column(String(), unique=True)
    document_type_name: Mapped[Optional[str]] = mapped_column(String())


class SellType(Base):
    __tablename__ = "sell_type"
    __table_args__ = {"schema": "main"}

    sell_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sell_type_code: Mapped[str] = mapped_column(String(), unique=True)
    sell_type_name: Mapped[Optional[str]] = mapped_column(String())


class CostCenter(Base):
    __tablename__ = "cost_center"
    __table_args__ = {"schema": "main"}

    cost_center_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cost_center_code: Mapped[str] = mapped_column(String(), unique=True)
    cost_center_name: Mapped[Optional[str]] = mapped_column(String())


class ProfitCenter(Base):
    __tablename__ = "profit_center"
    __table_args__ = {"schema": "main"}

    profit_center_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profit_center_code: Mapped[str] = mapped_column(String(), unique=True)
    profit_center_name: Mapped[Optional[str]] = mapped_column(String())


class ReturnType(Base):
    __tablename__ = "return_type"
    __table_args__ = {"schema": "main"}

    return_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    return_type_code: Mapped[str] = mapped_column(String(50), unique=True)
    return_type_name: Mapped[Optional[str]] = mapped_column(String(255))


class Uom(Base):
    __tablename__ = "uom"
    __table_args__ = {"schema": "main"}

    uom_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uom_code: Mapped[str] = mapped_column(String(50), unique=True)
    uom_name: Mapped[Optional[str]] = mapped_column(String(255))


class Transactions(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "main"}  

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    import_date: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default="NOW()"
    )
    
    business_partner_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.business_partner.business_partner_key"))
    product_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.product.product_key"))
    source_product_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.product.product_key"))
    document_type_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.document_type.document_type_key"))
    sell_type_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.sell_type.sell_type_key"))
    cost_center_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.cost_center.cost_center_key"))
    profit_center_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.profit_center.profit_center_key"))
    warehouse_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.warehouse.warehouse_key"))
    return_type_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.return_type.return_type_key"))
    uom_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.uom.uom_key"))
    
    document_no: Mapped[Optional[str]] = mapped_column(String())
    tax_code: Mapped[Optional[str]] = mapped_column(String())
    tax_number: Mapped[Optional[str]] = mapped_column(String())
    
    posting_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    demand_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    final_delivery_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    
    weight: Mapped[Optional[float]] = mapped_column(Numeric())
    uom_per_quantity: Mapped[Optional[float]] = mapped_column(Numeric())
    uom_quantity: Mapped[Optional[float]] = mapped_column(Numeric())
    quantity: Mapped[Optional[float]] = mapped_column(Numeric())
    quantity_packaging_uom: Mapped[Optional[float]] = mapped_column(Numeric())
    box: Mapped[Optional[float]] = mapped_column(Numeric())
    base_price: Mapped[Optional[float]] = mapped_column(Numeric())
    discount_percent: Mapped[Optional[float]] = mapped_column(Numeric())
    discounted_price: Mapped[Optional[float]] = mapped_column(Numeric())
    discounted_price_tax: Mapped[Optional[float]] = mapped_column(Numeric())
    revenue: Mapped[Optional[float]] = mapped_column(Numeric())
    main_amount_fc: Mapped[Optional[float]] = mapped_column(Numeric())
    amount: Mapped[Optional[float]] = mapped_column(Numeric())
    tax_amount_fc: Mapped[Optional[float]] = mapped_column(Numeric())
    amount_tax: Mapped[Optional[float]] = mapped_column(Numeric())
    amount_fc_tax: Mapped[Optional[float]] = mapped_column(Numeric())
    return_quantity: Mapped[Optional[float]] = mapped_column(Numeric())