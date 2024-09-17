import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-website-update-dialog',
  templateUrl: './website-update-dialog.component.html',
  styleUrls: ['./website-update-dialog.component.scss']
})
export class WebsiteUpdateDialogComponent {
  website: any;

  constructor(
    public dialogRef: MatDialogRef<WebsiteUpdateDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private apiService: ApiService
  ) {
    this.website = data.website;
  }

  onApply(): void {
    this.apiService.put(`/websites/${this.website.id}/`, this.website).subscribe(response => {
      this.dialogRef.close(this.website);
    });
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
