import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service'; // Import your ApiService
import { GroupeWebsiteDialogComponent } from '../groupewebsite-dialog/groupewebsite-dialog.component' ;

@Component({
  selector: 'app-website-dialog',
  templateUrl: './website-dialog.component.html',
  styleUrls: ['./website-dialog.component.scss']
})
export class WebsiteDialogComponent {
  websiteForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialog: MatDialog,
    public dialogRef: MatDialogRef<WebsiteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private apiService: ApiService // Inject your ApiService
    )
    {
      this.websiteForm = this.fb.group({
      nameWebsite: ['', Validators.required],
      url: ['', Validators.required],
      alerte: ['', Validators.required],
    });
  }

  onSubmit() {
    const website = {
      nameWebsite: this.websiteForm.value.nameWebSite,
      url: this.websiteForm.value.url,
      alerte : this.websiteForm.value.alerte
      // groupe_id: this.websiteForm.value.groupe,
    };
    console.log(website)
    this.apiService.post('/websites/', website).subscribe(
      response => {
        console.log('Data saved successfully', response);
        // Handle success
      },
      error => {
        console.error('Error saving data', error);
        // Handle error
      }
    );
  }

  openGroupeWebsiteDialog() {
    const dialogRef = this.dialog.open(GroupeWebsiteDialogComponent, {
      width: '350px',
      height :'220px'
      
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // User chose a group or created a new one
        // You can now add the group to the website object
        this.websiteForm.patchValue({ groupe: result });
      }
    });
  }
}