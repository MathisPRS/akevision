import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
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
    private apiService: ApiService
  ) {
    this.apiService.get('/groupes-websites/', { responseType: 'arraybuffer' }).subscribe(
      response => {
        const decoder = new TextDecoder('utf-8');
        const jsonString = decoder.decode(response);
        this.groups = JSON.parse(jsonString);
      },
      error => {
        console.error('Error fetching groups', error);
      }
    );
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
      this.dialogRef.close(this.selectedGroup);
    } else {
      // Close the dialog without returning a group ID
      this.dialogRef.close();
    }
  }
}