from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExcelFile, ColumnData, RowData
import json

def index(request):
    """Main page with dynamic dropdowns"""
    # Get the active Excel file
    active_file = ExcelFile.objects.filter(is_active=True).first()
    
    if not active_file:
        # No Excel file uploaded - show default column
        context = {
            'error': None,
            'no_excel': True,
            'default_column': {
                'name': 'Col 1',
                'values': ['Waiting for Excel']
            }
        }
        return render(request, 'main_app/index.html', context)
    
    # Get all columns for the active file (dynamic - any number of columns)
    columns = ColumnData.objects.filter(excel_file=active_file).order_by('id')
    
    context = {
        'columns': columns,
        'excel_file': active_file,
        'no_excel': False
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
            
            # Find the matching row - dynamic matching for any number of columns
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
            'name': col.column_name,  # Dynamic column name from Excel
            'values': col.get_unique_values()
        })
    
    rows_count = RowData.objects.filter(excel_file=active_file).count()
    
    return JsonResponse({
        'file_name': active_file.name,
        'columns': columns,
        'rows_count': rows_count
    })