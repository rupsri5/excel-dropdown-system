from django.db import models
import pandas as pd
import json

class ExcelFile(models.Model):
    """Model to store uploaded Excel files by admin"""
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/excel/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)  # Only one file can be active at a time
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} - {'Active' if self.is_active else 'Inactive'}"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Make sure only one file is active at a time
            ExcelFile.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
    
    def process_excel_data(self):
        """Process the Excel file and extract column data"""
        try:
            df = pd.read_excel(self.file.path)
            
            # Get all column names except 'total' (case insensitive)
            columns = [col for col in df.columns if col.lower() != 'total']
            total_column = None
            
            # Find the total column (case insensitive)
            for col in df.columns:
                if col.lower() == 'total':
                    total_column = col
                    break
            
            if not total_column:
                raise ValueError("No 'total' column found in the Excel file")
            
            # Clear existing data for this file
            ColumnData.objects.filter(excel_file=self).delete()
            RowData.objects.filter(excel_file=self).delete()
            
            # Create column data
            for column_name in columns:
                unique_values = df[column_name].dropna().unique().tolist()
                ColumnData.objects.create(
                    excel_file=self,
                    column_name=column_name,
                    unique_values=json.dumps(unique_values)
                )
            
            # Create row data for lookup
            for _, row in df.iterrows():
                row_values = {}
                for col in columns:
                    row_values[col] = str(row[col]) if pd.notna(row[col]) else ""
                
                RowData.objects.create(
                    excel_file=self,
                    values=json.dumps(row_values),
                    total_value=row[total_column] if pd.notna(row[total_column]) else 0
                )
            
            return True, "Excel file processed successfully"
        except Exception as e:
            return False, str(e)

class ColumnData(models.Model):
    """Model to store column names and their unique values"""
    excel_file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, related_name='columns')
    column_name = models.CharField(max_length=255)
    unique_values = models.TextField()  # JSON field to store unique values
    
    def get_unique_values(self):
        return json.loads(self.unique_values)
    
    def __str__(self):
        return f"{self.excel_file.name} - {self.column_name}"

class RowData(models.Model):
    """Model to store each row's data for lookup"""
    excel_file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, related_name='rows')
    values = models.TextField()  # JSON field to store row values
    total_value = models.FloatField()
    
    def get_values(self):
        return json.loads(self.values)
    
    def __str__(self):
        return f"{self.excel_file.name} - Total: {self.total_value}"
