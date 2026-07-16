import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import (
    String, Text, Date, Boolean, DateTime,
    ForeignKey, CheckConstraint, UniqueConstraint, Index, Numeric, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class sell_type_staging(Base):
    __tablename__ = "sell_type_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    sell_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.sell_type.sell_type_key")
    )


class DocumentTypeStaging(Base):
    __tablename__ = "document_type_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    document_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.document_type.document_type_key", ondelete="CASCADE")
    )


class CostCenterStaging(Base):
    __tablename__ = "cost_center_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    cost_center_key: Mapped[int] = mapped_column(
        ForeignKey("main.cost_center.cost_center_key", ondelete="CASCADE")
    )


class ProfitCenterStaging(Base):
    __tablename__ = "profit_center_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    profit_center_key: Mapped[int] = mapped_column(
        ForeignKey("main.profit_center.profit_center_key", ondelete="CASCADE")
    )


class WarehouseStaging(Base):
    __tablename__ = "warehouse_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    warehouse_key: Mapped[int] = mapped_column(
        ForeignKey("main.warehouse.warehouse_key", ondelete="CASCADE")
    )


class ReturnTypeStaging(Base):
    __tablename__ = "return_type_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    return_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.return_type.return_type_key", ondelete="CASCADE")
    )


class UomStaging(Base):
    __tablename__ = "uom_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    uom_key: Mapped[int] = mapped_column(
        ForeignKey("main.uom.uom_key", ondelete="CASCADE")
    )

class TaxStaging(Base):
    __tablename__ = "tax_staging"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    raw_value: Mapped[str] = mapped_column(String, unique=True)
    tax_key: Mapped[int] = mapped_column(
        ForeignKey("main.tax.tax_key", ondelete="CASCADE")
    )


class TransactionsStaging(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    import_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    business_partner_code: Mapped[Optional[str]] = mapped_column(String)
    business_partner_name: Mapped[Optional[str]] = mapped_column(String)
    province_name: Mapped[Optional[str]] = mapped_column(String)
    team_name: Mapped[Optional[str]] = mapped_column(String)
    branch_name: Mapped[Optional[str]] = mapped_column(String)
    bp_group_name: Mapped[Optional[str]] = mapped_column(String)
    product_code: Mapped[Optional[str]] = mapped_column(String)
    product_name: Mapped[Optional[str]] = mapped_column(String)
    source_product_code: Mapped[Optional[str]] = mapped_column(String)
    source_product_name: Mapped[Optional[str]] = mapped_column(String)
    document_type_name: Mapped[Optional[str]] = mapped_column(String)
    sell_type_name: Mapped[Optional[str]] = mapped_column(String)
    cost_center_code: Mapped[Optional[str]] = mapped_column(String)
    cost_center_name: Mapped[Optional[str]] = mapped_column(String)
    profit_center_code: Mapped[Optional[str]] = mapped_column(String)
    profit_center_name: Mapped[Optional[str]] = mapped_column(String)
    warehouse_code: Mapped[Optional[str]] = mapped_column(String)
    warehouse_name: Mapped[Optional[str]] = mapped_column(String)
    return_type_code: Mapped[Optional[str]] = mapped_column(String)
    return_type_name: Mapped[Optional[str]] = mapped_column(String)
    uom_name: Mapped[Optional[str]] = mapped_column(String)
    tax_code: Mapped[Optional[str]] = mapped_column(String)
    document_no: Mapped[Optional[str]] = mapped_column(String)
    tax_number: Mapped[Optional[str]] = mapped_column(String)

    posting_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    demand_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    final_delivery_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    weight: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    uom_per_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    uom_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity_packaging_uom: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    box: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    base_price: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discount_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discounted_price: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discounted_price_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_revenue: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_fc: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_amount_fc: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_fc_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    return_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    remark: Mapped[Optional[str]] = mapped_column(Text)
    source_file: Mapped[Optional[str]] = mapped_column(Text)
    scenario: Mapped[Optional[str]] = mapped_column(Text)


class Dept(Base):
    __tablename__ = "dept"
    __table_args__ = {"schema": "main"}

    dept_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dept_name: Mapped[str] = mapped_column(String)

    teams: Mapped[List["Team"]] = relationship(back_populates="dept")


class Channel(Base):
    __tablename__ = "channel"
    __table_args__ = {"schema": "main"}

    channel_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_name: Mapped[str] = mapped_column(String)

    branches: Mapped[List["Branch"]] = relationship(back_populates="channel")


class Branch(Base):
    __tablename__ = "branch"
    __table_args__ = {"schema": "main"}

    branch_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    branch_name: Mapped[str] = mapped_column(String)
    
    dept_key: Mapped[int] = mapped_column(ForeignKey("main.dept.dept_key"))
    channel_key: Mapped[int] = mapped_column(ForeignKey("main.channel.channel_key"))

    channel: Mapped["Channel"] = relationship(back_populates="branches")
    teams: Mapped[List["Team"]] = relationship(back_populates="branch")


class Team(Base):
    __tablename__ = "team"
    __table_args__ = {"schema": "main"}

    team_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_name: Mapped[str] = mapped_column(String)
    branch_key: Mapped[int] = mapped_column(ForeignKey("main.branch.branch_key"))

    branch: Mapped["Branch"] = relationship(back_populates="teams")
    dept: Mapped[Optional["Dept"]] = relationship(back_populates="teams")

    business_partners: Mapped[List["BusinessPartner"]] = relationship(back_populates="team")

class KpiGroup(Base):
    __tablename__ = "kpi_group"
    __table_args__ = {"schema": "main"}

    kpi_group_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sub_kpi_0: Mapped[Optional[str]] = mapped_column(String)
    sub_kpi_1: Mapped[Optional[str]] = mapped_column(String)
    sub_kpi_2: Mapped[Optional[str]] = mapped_column(String)
    sub_kpi_3: Mapped[Optional[str]] = mapped_column(String)

    product_categories: Mapped[List["ProductCategory"]] = relationship(back_populates="kpi_group")


class Market(Base):
    __tablename__ = "market"
    __table_args__ = {"schema": "main"}

    market_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    market_type_name: Mapped[str] = mapped_column(String)
    country_name_eng: Mapped[str] = mapped_column(String)
    country_shortname_a2: Mapped[str] = mapped_column(String)
    country_name_vi: Mapped[Optional[str]] = mapped_column(String)

    products: Mapped[List["Product"]] = relationship(back_populates="market")


class ProductCategory(Base):
    __tablename__ = "product_category"
    __table_args__ = {"schema": "main"}

    product_category_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_category_name: Mapped[Optional[str]] = mapped_column(String)
    kpi_group_key: Mapped[Optional[int]] = mapped_column(ForeignKey("main.kpi_group.kpi_group_key"))

    kpi_group: Mapped[Optional["KpiGroup"]] = relationship(back_populates="product_categories")
    products: Mapped[List["Product"]] = relationship(back_populates="product_category")


class MsgGroup(Base):
    __tablename__ = "msg_group"
    __table_args__ = {"schema": "main"}

    msg_group_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    msg_group_name: Mapped[str] = mapped_column(String, unique=True)
    msg_group_size: Mapped[str] = mapped_column(String)

    products: Mapped[List["Product"]] = relationship(back_populates="msg_group")


class DucvietCategoryGroup(Base):
    __tablename__ = "ducviet_category_group"
    __table_args__ = {"schema": "main"}

    ducviet_category_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ducviet_category_name: Mapped[str] = mapped_column(String, unique=True)

    products: Mapped[List["Product"]] = relationship(back_populates="ducviet_category_group")


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "main"}

    product_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(String)
    product_name: Mapped[Optional[str]] = mapped_column(String)
    product_name_eng: Mapped[Optional[str]] = mapped_column(String)
    product_category_key: Mapped[int] = mapped_column(
        ForeignKey("main.product_category.product_category_key")
    )
    market_key: Mapped[int] = mapped_column(
        ForeignKey("main.market.market_key"), 
        server_default="1" 
    )
    msg_group_key: Mapped[int] = mapped_column(
        ForeignKey("main.msg_group.msg_group_key")
    )
    ducviet_category_key: Mapped[int] = mapped_column(
        ForeignKey("main.ducviet_category_group.ducviet_category_key")
    )
    imported_date: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.now()
    )

    product_category: Mapped["ProductCategory"] = relationship(back_populates="products")
    market: Mapped["Market"] = relationship(back_populates="products")
    msg_group: Mapped["MsgGroup"] = relationship(back_populates="products")
    ducviet_category_group: Mapped["DucvietCategoryGroup"] = relationship(back_populates="products")


class Warehouse(Base):
    __tablename__ = "warehouse"
    __table_args__ = {"schema": "main"}

    warehouse_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    warehouse_code: Mapped[str] = mapped_column(String, unique=True)
    warehouse_name: Mapped[str] = mapped_column(String)


class Province(Base):
    __tablename__ = "province"
    __table_args__ = {"schema": "main"}

    province_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    province_name_old: Mapped[str] = mapped_column(String, unique=True)
    province_name_new: Mapped[str] = mapped_column(String)
    
    business_partners: Mapped[List["BusinessPartner"]] = relationship(back_populates="province")


class BusinessPartnerType(Base):
    __tablename__ = "business_partner_type"
    __table_args__ = {"schema": "main"}

    bp_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bp_type_name: Mapped[Optional[str]] = mapped_column(String)

    groups: Mapped[List["BusinessPartnerGroup"]] = relationship(back_populates="partner_type")


class BusinessPartnerGroup(Base):
    __tablename__ = "business_partner_group"
    __table_args__ = {"schema": "main"}

    bp_group_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bp_group_name: Mapped[Optional[str]] = mapped_column(String)
    bp_type_key: Mapped[int] = mapped_column(ForeignKey("main.business_partner_type.bp_type_key"))

    partner_type: Mapped[Optional["BusinessPartnerType"]] = relationship(back_populates="groups")
    partners: Mapped[List["BusinessPartner"]] = relationship(back_populates="partner_group")


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
    business_partner_name: Mapped[Optional[str]] = mapped_column(String)
    bp_group_key: Mapped[int] = mapped_column(
        ForeignKey("main.business_partner_group.bp_group_key", ondelete="RESTRICT")
    )
    team_key: Mapped[int] = mapped_column(
        ForeignKey("main.team.team_key", ondelete="RESTRICT")
    )
    province_key: Mapped[int] = mapped_column(
        ForeignKey("main.province.province_key", ondelete="RESTRICT")
    )
    creation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    import_date: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    valid_from: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.date_trunc("month", func.now())
    )
    valid_to: Mapped[Optional[datetime.date]] = mapped_column(Date) 
    is_current: Mapped[bool] = mapped_column(Boolean, server_default="true")

    partner_group: Mapped["BusinessPartnerGroup"] = relationship(back_populates="partners")
    team: Mapped["Team"] = relationship(back_populates="business_partners")
    province: Mapped["Province"] = relationship(back_populates="business_partners")


class DocumentType(Base):
    __tablename__ = "document_type"
    __table_args__ = {"schema": "main"}

    document_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_type_name: Mapped[Optional[str]] = mapped_column(String)


class SellType(Base):
    __tablename__ = "sell_type"
    __table_args__ = {"schema": "main"}

    sell_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sell_type_name: Mapped[Optional[str]] = mapped_column(String)


class CostCenter(Base):
    __tablename__ = "cost_center"
    __table_args__ = {"schema": "main"}

    cost_center_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cost_center_code: Mapped[str] = mapped_column(String, unique=True)
    cost_center_name: Mapped[Optional[str]] = mapped_column(String)


class ProfitCenter(Base):
    __tablename__ = "profit_center"
    __table_args__ = {"schema": "main"}

    profit_center_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profit_center_code: Mapped[str] = mapped_column(String, unique=True)
    profit_center_name: Mapped[Optional[str]] = mapped_column(String)


class ReturnType(Base):
    __tablename__ = "return_type"
    __table_args__ = {"schema": "main"}

    return_type_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    return_type_code: Mapped[str] = mapped_column(String, unique=True)
    return_type_name: Mapped[Optional[str]] = mapped_column(String)


class Uom(Base):
    __tablename__ = "uom"
    __table_args__ = {"schema": "main"}

    uom_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uom_name: Mapped[str] = mapped_column(String, unique=True)


class Tax(Base):
    __tablename__ = "tax"
    __table_args__ = {"schema": "main"}

    tax_key: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tax_code: Mapped[str] = mapped_column(String, unique=True)


class Transactions(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "main"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    import_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    business_partner_key: Mapped[int] = mapped_column(
        ForeignKey("main.business_partner.business_partner_key", ondelete="RESTRICT")
    )
    product_key: Mapped[int] = mapped_column(
        ForeignKey("main.product.product_key", ondelete="RESTRICT")
    )
    source_product_key: Mapped[int] = mapped_column(
        ForeignKey("main.product.product_key", ondelete="RESTRICT")
    )
    document_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.document_type.document_type_key", ondelete="RESTRICT")
    )
    sell_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.sell_type.sell_type_key", ondelete="RESTRICT")
    )
    cost_center_key: Mapped[int] = mapped_column(
        ForeignKey("main.cost_center.cost_center_key", ondelete="RESTRICT")
    )
    profit_center_key: Mapped[int] = mapped_column(
        ForeignKey("main.profit_center.profit_center_key", ondelete="RESTRICT")
    )
    warehouse_key: Mapped[int] = mapped_column(
        ForeignKey("main.warehouse.warehouse_key", ondelete="RESTRICT")
    )
    return_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.return_type.return_type_key", ondelete="RESTRICT")
    )
    uom_key: Mapped[int] = mapped_column(
        ForeignKey("main.uom.uom_key", ondelete="RESTRICT")
    )
    tax_key: Mapped[int] = mapped_column(
        ForeignKey("main.tax.tax_key", ondelete="RESTRICT")
    )

    document_no: Mapped[Optional[str]] = mapped_column(String)
    tax_number: Mapped[Optional[str]] = mapped_column(String)
    
    posting_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    demand_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    final_delivery_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    weight: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    uom_per_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    uom_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity_packaging_uom: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    box: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    base_price: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discount_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discounted_price: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discounted_price_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_revenue: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_fc: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_amount_fc: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_fc_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    return_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)

    business_partner: Mapped["BusinessPartner"] = relationship()
    product: Mapped["Product"] = relationship(foreign_keys=[product_key])
    source_product: Mapped["Product"] = relationship(foreign_keys=[source_product_key])
    document_type: Mapped["DocumentType"] = relationship()
    sell_type: Mapped["SellType"] = relationship()
    cost_center: Mapped["CostCenter"] = relationship()
    profit_center: Mapped["ProfitCenter"] = relationship()
    warehouse: Mapped["Warehouse"] = relationship()
    return_type: Mapped["ReturnType"] = relationship()
    uom: Mapped["Uom"] = relationship() 


class TransactionsDaily(Base):
    __tablename__ = "transactions_daily"
    __table_args__ = {"schema": "main"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    import_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    business_partner_key: Mapped[int] = mapped_column(
        ForeignKey("main.business_partner.business_partner_key", ondelete="RESTRICT")
    )
    product_key: Mapped[int] = mapped_column(
        ForeignKey("main.product.product_key", ondelete="RESTRICT")
    )
    source_product_key: Mapped[int] = mapped_column(
        ForeignKey("main.product.product_key", ondelete="RESTRICT")
    )
    document_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.document_type.document_type_key", ondelete="RESTRICT")
    )
    sell_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.sell_type.sell_type_key", ondelete="RESTRICT")
    )
    cost_center_key: Mapped[int] = mapped_column(
        ForeignKey("main.cost_center.cost_center_key", ondelete="RESTRICT")
    )
    profit_center_key: Mapped[int] = mapped_column(
        ForeignKey("main.profit_center.profit_center_key", ondelete="RESTRICT")
    )
    warehouse_key: Mapped[int] = mapped_column(
        ForeignKey("main.warehouse.warehouse_key", ondelete="RESTRICT")
    )
    return_type_key: Mapped[int] = mapped_column(
        ForeignKey("main.return_type.return_type_key", ondelete="RESTRICT")
    )
    uom_key: Mapped[int] = mapped_column(
        ForeignKey("main.uom.uom_key", ondelete="RESTRICT")
    )
    tax_key: Mapped[int] = mapped_column(
        ForeignKey("main.tax.tax_key", ondelete="RESTRICT")
    )

    document_no: Mapped[Optional[str]] = mapped_column(String)
    tax_number: Mapped[Optional[str]] = mapped_column(String)
    
    posting_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    demand_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    final_delivery_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    weight: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    uom_per_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    uom_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity_packaging_uom: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    box: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    base_price: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discount_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discounted_price: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    discounted_price_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_revenue: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_fc: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_amount_fc: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_amount_fc_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    return_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)

    business_partner: Mapped["BusinessPartner"] = relationship()
    product: Mapped["Product"] = relationship(foreign_keys=[product_key])
    source_product: Mapped["Product"] = relationship(foreign_keys=[source_product_key])
    document_type: Mapped["DocumentType"] = relationship()
    sell_type: Mapped["SellType"] = relationship()
    cost_center: Mapped["CostCenter"] = relationship()
    profit_center: Mapped["ProfitCenter"] = relationship()
    warehouse: Mapped["Warehouse"] = relationship()
    return_type: Mapped["ReturnType"] = relationship()
    uom: Mapped["Uom"] = relationship() 


class ProfitAndLossStaging(Base):
    __tablename__ = "profit_and_loss"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    profit_center_code: Mapped[Optional[str]] = mapped_column(String)
    business_partner_code: Mapped[Optional[str]] = mapped_column(String)
    product_code: Mapped[Optional[str]] = mapped_column(String)
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    a_non_operating_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    a_non_operating_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    administrative_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    advertise_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    bank_transfer_fee_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    communication_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    communication_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    cost_of_good_sold: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    cost_of_good_sold_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    delivery_maint_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    depreciation_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    depreciation_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    entertainment_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    entertainment_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    expenses_from_provisions_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    export_transportation_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    extraordinary_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    extraordinary_incomes: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    financial_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    financial_rev_exp: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    financial_revenue: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    fx_loss_realized: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    gross_profit: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    house_renting_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    income_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    land_renting_expense_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    management_service_fee_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    net_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    office_salaries_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    offices_supplies_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    offices_supplies_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    oil_fee_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    operating_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    operating_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    ordinary_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_expenses_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_expenses_by_cash_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_repair_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_services_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    porters_fee_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    provision_for_decline: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity_inventory_uom: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity_net: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    repair_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    salary_allowance_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sale_promotions_item: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sale_promotions_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_net: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    school_medical_fee_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    selling_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_fees_and_charges_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tools_equipment_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    training_education_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    transportation_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    travelling_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    travelling_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    water_lighting_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    water_lighting_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    
    
class ProfitAndLoss(Base):
    __tablename__ = "profit_and_loss"
    __table_args__ = {"schema": "main"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    profit_center_key: Mapped[Optional[int]] = mapped_column(
        ForeignKey("main.profit_center.profit_center_key", ondelete="RESTRICT")
    )
    business_partner_key: Mapped[Optional[int]] = mapped_column(
        ForeignKey("main.business_partner.business_partner_key", ondelete = "RESTRICT")
    )
    product_key: Mapped[Optional[int]] = mapped_column(
        ForeignKey("main.product.product_key", ondelete="RESTRICT")
    )
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    a_non_operating_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    a_non_operating_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    administrative_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    advertise_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    bank_transfer_fee_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    communication_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    communication_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    cost_of_good_sold: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    cost_of_good_sold_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    delivery_maint_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    depreciation_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    depreciation_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    entertainment_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    entertainment_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    expenses_from_provisions_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    export_transportation_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    extraordinary_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    extraordinary_incomes: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    financial_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    financial_rev_exp: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    financial_revenue: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    fx_loss_realized: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    gross_profit: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    house_renting_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    income_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    land_renting_expense_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    management_service_fee_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    net_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    office_salaries_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    offices_supplies_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    offices_supplies_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    oil_fee_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    operating_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    operating_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    ordinary_income: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_expenses_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_expenses_by_cash_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_repair_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    other_services_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    porters_fee_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    provision_for_decline: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity_inventory_uom: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    quantity_net: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    repair_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    salary_allowance_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sale_promotions_item: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sale_promotions_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    sales_net: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    school_medical_fee_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    selling_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tax_fees_and_charges_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    tools_equipment_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    training_education_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    transportation_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    travelling_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    travelling_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    water_lighting_a: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    water_lighting_s: Mapped[Optional[Decimal]] = mapped_column(Numeric)