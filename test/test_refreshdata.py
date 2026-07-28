import win32com.client as win32

excel = win32.Dispatch("Excel.Application")
excel.Visible = True 
wb_path = [
    r"D:\OneDrive - 6005jb\Daesang\4. Data Exports\28.07.2026_Doanh số_2025 - 2026.xlsx",
    r"D:\OneDrive - 6005jb\Daesang\4. Data Exports\28.07.2026_Ms.Yến_OP (Chia XK).xlsx"
]

for path in wb_path:
    wb = excel.Workbooks.Open(path)

    wb.RefreshAll()

    excel.CalculateUntilAsyncQueriesDone()

    wb.Save()
    wb.Close()

excel.Quit()