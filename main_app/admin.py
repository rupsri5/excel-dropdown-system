from django.contrib import admin
from django.contrib import messages
from .models import ExcelFile, ColumnData, RowData

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at', 'is_active', 'file']
    list_filter = ['is_active', 'uploaded_at']
    search_fields = ['name']
    readonly_fields = ['uploaded_at']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Process the Excel file after saving
        success, message = obj.process_excel_data()
        if success:
            messages.success(request, f"Excel file '{obj.name}' processed successfully!")
        else:
            messages.error(request, f"Error processing Excel file: {message}")

@admin.register(ColumnData)
class ColumnDataAdmin(admin.ModelAdmin):
    list_display = ['excel_file', 'column_name', 'unique_values_preview']
    list_filter = ['excel_file', 'column_name']
    search_fields = ['column_name', 'excel_file__name']
    
    def unique_values_preview(self, obj):
        values = obj.get_unique_values()
        if len(values) > 3:
            return f"{', '.join(map(str, values[:3]))}... ({len(values)} total)"
        return ', '.join(map(str, values))
    unique_values_preview.short_description = 'Unique Values Preview'

@admin.register(RowData)
class RowDataAdmin(admin.ModelAdmin):
    list_display = ['excel_file', 'values_preview', 'total_value']
    list_filter = ['excel_file']
    search_fields = ['excel_file__name']
    
    def values_preview(self, obj):
        values = obj.get_values()
        items = list(values.items())
        if len(items) > 2:
            preview = f"{items[0][0]}:{items[0][1]}, {items[1][0]}:{items[1][1]}..."
        else:
            preview = ', '.join([f"{k}:{v}" for k, v in items])
        return preview
    values_preview.short_description = 'Values Preview'
'''

print("=== admin.py ===")
print(admin_content)

# Create views.py content
views_content = '''
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExcelFile, ColumnData, RowData
import json

def index(request):
    """Main page with dropdowns"""
    # Get the active Excel file
    active_file = ExcelFile.objects.filter(is_active=True).first()
    
    if not active_file:
        return render(request, 'main_app/index.html', {
            'error': 'No active Excel file found. Please contact admin to upload a file.'
        })
    
    # Get all columns for the active file
    columns = ColumnData.objects.filter(excel_file=active_file).order_by('id')
    
    context = {
        'columns': columns,
        'excel_file': active_file
    }
    
    return render(request, 'main_app/index.html', context)

@csrf_exempt
def get_total_value(request):
    """AJAX endpoint to get total value based on selected dropdown values"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selections = data.get('selections', {})
            
            # Get the active Excel file
            active_file = ExcelFile.objects.filter(is_active=True).first()
            
            if not active_file:
                return JsonResponse({'error': 'No active Excel file found'}, status=404)
            
            # Find the matching row
            for row in RowData.objects.filter(excel_file=active_file):
                row_values = row.get_values()
                
                # Check if all selections match this row
                match = True
                for column, value in selections.items():
                    if str(row_values.get(column, '')) != str(value):
                        match = False
                        break
                
                if match:
                    return JsonResponse({
                        'total': row.total_value,
                        'success': True
                    })
            
            return JsonResponse({
                'error': 'No matching combination found',
                'success': False
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'error': f'Server error: {str(e)}',
                'success': False
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def test_data(request):
    """Test endpoint to check if data is loaded properly"""
    active_file = ExcelFile.objects.filter(is_active=True).first()
    
    if not active_file:
        return JsonResponse({'error': 'No active file'})
    
    columns = []
    for col in ColumnData.objects.filter(excel_file=active_file):
        columns.append({
            'name': col.column_name,
            'values': col.get_unique_values()
        })
    
    rows_count = RowData.objects.filter(excel_file=active_file).count()
    
    return JsonResponse({
        'file_name': active_file.name,
        'columns': columns,
        'rows_count': rows_count
    })