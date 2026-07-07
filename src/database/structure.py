import datetime
from sqlalchemy import (
    Numeric, String, Date, DateTime, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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
    sales_uom_name: Mapped[str | None] = mapped_column(String(50))
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
    sales_revenue: Mapped[float | None] = mapped_column(Numeric(15, 4))
    sales_amount_fc: Mapped[float | None] = mapped_column(Numeric(15, 4))
    tax_amount: Mapped[float | None] = mapped_column(Numeric(15, 4))
    tax_amount_fc: Mapped[float | None] = mapped_column(Numeric(15, 4))
    sales_amount_tax: Mapped[float | None] = mapped_column(Numeric(15, 4))
    sales_amount_fc_tax: Mapped[float | None] = mapped_column(Numeric(15, 4))
    return_quantity: Mapped[float | None] = mapped_column(Numeric(15, 4))