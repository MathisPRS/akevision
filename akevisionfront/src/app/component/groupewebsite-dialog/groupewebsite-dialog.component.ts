// groupe-website-dialog.component.ts
import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from '../../services/api.service'; // Import your ApiService

@Component({
  selector: 'app-groupe-website-dialog',
  templateUrl: './groupewebsite-dialog.component.html',
  styleUrls: ['./groupewebsite-dialog.component.scss']
})
export class GroupeWebsiteDialogComponent {
  groupeName: string;
  selectedGroup: number;
  groups: any[];

  constructor(
    public dialogRef: MatDialogRef<GroupeWebsiteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private apiService: ApiService
  ) {
    this.groups = data.groups;
  }

  closeDialog() {
    if (this.groupeName) {
      // Create a new group and return its ID
      this.apiService.post('/groupes-websites/', { name: this.groupeName }).subscribe(
        response => {
          this.dialogRef.close(response);
        },
        error => {
          console.error('Error creating group', error);
        }
      );
    } else if (this.selectedGroup) {
      // Return the selected group ID
      this.dialogRef.close(this.groups.find(group => group.id === this.selectedGroup));
    } else {
      // Close the dialog without returning a group ID
      this.dialogRef.close();
    }
  }
}