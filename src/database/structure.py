from typing import Optional
import datetime
from sqlalchemy import (
    Numeric, String, Date, DateTime,ForeignKey, func
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
    
    business_partner_code: Mapped[str | None] = mapped_column(String(50))
    business_partner_name: Mapped[str | None] = mapped_column(String(255))
    team_name: Mapped[str | None] = mapped_column(String(50))
    branch_name: Mapped[str | None] = mapped_column(String(50))
    bp_group_name: Mapped[str | None] = mapped_column(String(50))
    product_code: Mapped[str | None] = mapped_column(String(50))
    product_name: Mapped[str | None] = mapped_column(String(255))
    source_product_code: Mapped[str | None] = mapped_column(String(50))
    source_product_name: Mapped[str | None] = mapped_column(String(255))
    document_type_name: Mapped[str | None] = mapped_column(String(50))
    sell_type_name: Mapped[str | None] = mapped_column(String(50))
    cost_center_code: Mapped[str | None] = mapped_column(String(50))
    cost_center_name: Mapped[str | None] = mapped_column(String(255))
    profit_center_code: Mapped[str | None] = mapped_column(String(50))
    profit_center_name: Mapped[str | None] = mapped_column(String(255))
    warehouse_code: Mapped[str | None] = mapped_column(String(50))
    warehouse_name: Mapped[str | None] = mapped_column(String(255))
    return_type_code: Mapped[str | None] = mapped_column(String(50))
    return_type_name: Mapped[str | None] = mapped_column(String(255))
    main_uom_name: Mapped[str | None] = mapped_column(String(50))
    document_no: Mapped[str | None] = mapped_column(String(50))
    tax_code: Mapped[str | None] = mapped_column(String(50))
    tax_number: Mapped[str | None] = mapped_column(String(50))
    
    posting_date: Mapped[datetime.date | None] = mapped_column(Date)
    due_date: Mapped[datetime.date | None] = mapped_column(Date)
    demand_date: Mapped[datetime.date | None] = mapped_column(Date)
    final_delivery_date: Mapped[datetime.date | None] = mapped_column(Date)
    
    weight: Mapped[float | None] = mapped_column(Numeric(15, 4))
    uom_per_quantity: Mapped[float | None] = mapped_column(Numeric(15, 4))
    uom_quantity: Mapped[float | None] = mapped_column(Numeric(15, 4))
    quantity: Mapped[float | None] = mapped_column(Numeric(15, 4))
    quantity_packaging_uom: Mapped[float | None] = mapped_column(Numeric(15, 4))
    box: Mapped[float | None] = mapped_column(Numeric(15, 4))
    base_price: Mapped[float | None] = mapped_column(Numeric(15, 4))
    discount_percent: Mapped[float | None] = mapped_column(Numeric(15, 2))
    discounted_price: Mapped[float | None] = mapped_column(Numeric(15, 4))
    discounted_price_tax: Mapped[float | None] = mapped_column(Numeric(15, 4))
    main_revenue: Mapped[float | None] = mapped_column(Numeric(15, 4))
    main_amount_fc: Mapped[float | None] = mapped_column(Numeric(15, 4))
    tax_amount: Mapped[float | None] = mapped_column(Numeric(15, 4))
    tax_amount_fc: Mapped[float | None] = mapped_column(Numeric(15, 4))
    main_amount_tax: Mapped[float | None] = mapped_column(Numeric(15, 4))
    main_amount_fc_tax: Mapped[float | None] = mapped_column(Numeric(15, 4))
    return_quantity: Mapped[float | None] = mapped_column(Numeric(15, 4))
    remark: Mapped[str | None] = mapped_column(String(255))


class Dept(Base):
    __tablename__ = "dept"
    __table_args__ = {"schema": "main"}

    dept_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dept_name: Mapped[str] = mapped_column(String(50))

    teams: Mapped[list["Team"]] = relationship(back_populates="dept")


class Channel(Base):
    __tablename__ = "channel"
    __table_args__ = {"schema": "main"}

    channel_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_name: Mapped[str] = mapped_column(String(50))

    branches: Mapped[list["Branch"]] = relationship(back_populates="channel")


class Branch(Base):
    __tablename__ = "branch"
    __table_args__ = {"schema": "main"}

    branch_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    branch_name: Mapped[str] = mapped_column(String(50))
    
    channel_key: Mapped[int] = mapped_column(ForeignKey("main.channel.channel_key"))

    channel: Mapped["Channel"] = relationship(back_populates="branches")
    teams: Mapped[list["Team"]] = relationship(back_populates="branch")


class Team(Base):
    __tablename__ = "team"
    __table_args__ = {"schema": "main"}

    team_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_name: Mapped[str] = mapped_column(String(50))
    
    branch_key: Mapped[int] = mapped_column(ForeignKey("main.branch.branch_key"))
    dept_key: Mapped[int] = mapped_column(ForeignKey("main.dept.dept_key"))

    branch: Mapped["Branch"] = relationship(back_populates="teams") 
    dept: Mapped["Dept"] = relationship(back_populates="teams")


class KpiGroup(Base):
    __tablename__ = "kpi_group"
    __table_args__ = {"schema": "main"}

    kpi_group_key: Mapped[int] = mapped_column(primary_key=True)
    sub_kpi_1: Mapped[Optional[str]] = mapped_column(String(20))
    sub_kpi_2: Mapped[Optional[str]] = mapped_column(String(20))
    sub_kpi_3: Mapped[Optional[str]] = mapped_column(String(20))
    sub_kpi_0: Mapped[Optional[str]] = mapped_column(String(20))

    product_categories: Mapped[list["ProductCategory"]] = relationship(back_populates="kpi_group")


class Market(Base):
    __tablename__ = "market"
    __table_args__ = {"schema": "main"}

    market_key: Mapped[int] = mapped_column(primary_key=True)
    market_type: Mapped[str] = mapped_column(String(30))
    country_name_eng: Mapped[str] = mapped_column(String(30))
    country_shortname_a2: Mapped[str] = mapped_column(String(2))
    country_name_vi: Mapped[Optional[str]] = mapped_column(String(50))

    products: Mapped[list["Product"]] = relationship(back_populates="market")


class ProductCategory(Base):
    __tablename__ = "product_category"
    __table_args__ = {"schema": "main"}

    product_category_key: Mapped[int] = mapped_column(primary_key=True)
    product_category_name: Mapped[Optional[str]] = mapped_column(String(30))
    kpi_group_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.kpi_group.kpi_group_key"))
    product_category_name_eng: Mapped[Optional[str]] = mapped_column()

    kpi_group: Mapped[Optional["KpiGroup"]] = relationship(back_populates="product_categories")
    products: Mapped[list["Product"]] = relationship(back_populates="product_category")


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "main"}

    product_key: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column()
    product_name: Mapped[Optional[str]] = mapped_column(String(100))
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
    warehouse_code: Mapped[int] = mapped_column(String(50), unique=True)
    warehouse_name: Mapped[int] = mapped_column(String(255))

class BusinessPartnerGroup(Base):
    __tablename__ = "business_partner_group"
    __table_args__ = {"schema": "sales"}

    bp_group_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bp_group_code: Mapped[str] = mapped_column(String(50), unique=True)
    bp_group_name: Mapped[Optional[str]] = mapped_column(String(255))


class DocumentType(Base):
    __tablename__ = "document_type"
    __table_args__ = {"schema": "sales"}

    document_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_type_code: Mapped[str] = mapped_column(String(50), unique=True)
    document_type_name: Mapped[Optional[str]] = mapped_column(String(255))


class SellType(Base):
    __tablename__ = "sell_type"
    __table_args__ = {"schema": "sales"}

    sell_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sell_type_code: Mapped[str] = mapped_column(String(50), unique=True)
    sell_type_name: Mapped[Optional[str]] = mapped_column(String(255))


class CostCenter(Base):
    __tablename__ = "cost_center"
    __table_args__ = {"schema": "sales"}

    cost_center_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cost_center_code: Mapped[str] = mapped_column(String(50), unique=True)
    cost_center_name: Mapped[Optional[str]] = mapped_column(String(255))


class ProfitCenter(Base):
    __tablename__ = "profit_center"
    __table_args__ = {"schema": "sales"}

    profit_center_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profit_center_code: Mapped[str] = mapped_column(String(50), unique=True)
    profit_center_name: Mapped[Optional[str]] = mapped_column(String(255))


class ReturnType(Base):
    __tablename__ = "return_type"
    __table_args__ = {"schema": "sales"}

    return_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    return_type_code: Mapped[str] = mapped_column(String(50), unique=True)
    return_type_name: Mapped[Optional[str]] = mapped_column(String(255))


class Uom(Base):
    __tablename__ = "uom"
    __table_args__ = {"schema": "sales"}

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
    
    business_partner_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.business_partner.business_partner_key"))
    team_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.team.team_key"))
    branch_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.branch.branch_key"))
    bp_group_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.business_partner_group.bp_group_key"))
    product_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.product.product_key"))
    source_product_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.product.product_key"))
    document_type_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.document_type.document_type_key"))
    sell_type_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.sell_type.sell_type_key"))
    cost_center_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.cost_center.cost_center_key"))
    profit_center_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.profit_center.profit_center_key"))
    warehouse_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.warehouse.warehouse_key"))
    return_type_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.return_type.return_type_key"))
    uom_key: Mapped[Optional[int]] = mapped_column(ForeignKey("sales.uom.uom_key"))
    
    document_no: Mapped[Optional[str]] = mapped_column(String(50))
    tax_code: Mapped[Optional[str]] = mapped_column(String(50))
    tax_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    posting_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    demand_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    final_delivery_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    
    weight: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    uom_per_quantity: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    uom_quantity: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    quantity: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    quantity_packaging_uom: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    box: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    base_price: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    discount_percent: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    discounted_price: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    discounted_price_tax: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    main_revenue: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    main_amount_fc: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    tax_amount: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    tax_amount_fc: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    main_amount_tax: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    main_amount_fc_tax: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    return_quantity: Mapped[Optional[float]] = mapped_column(Numeric(15, 4))
    remark: Mapped[Optional[str]] = mapped_column(String(255))