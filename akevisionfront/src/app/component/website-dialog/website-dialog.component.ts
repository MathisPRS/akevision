// website-dialog.component.ts
import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service'; // Import your ApiService
import { GroupeWebsiteDialogComponent } from '../groupewebsite-dialog/groupewebsite-dialog.component' ;
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-website-dialog',
  templateUrl: './website-dialog.component.html',
  styleUrls: ['./website-dialog.component.scss']
})
export class WebsiteDialogComponent {
  websiteForm: FormGroup;
  groups: any[];
  selectedGroupName: string;

  constructor(
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private dialog: MatDialog,
    public dialogRef: MatDialogRef<WebsiteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private apiService: ApiService // Inject your ApiService
  ) {
    this.websiteForm = this.fb.group({
      nameWebsite: ['', Validators.required],
      url: ['', Validators.required],
      alerte: ['', Validators.required],
    });
  }

  onSubmit() {
    const website = {
      nameWebsite: this.websiteForm.value.nameWebsite,
      url: this.websiteForm.value.url,
      alerte : this.websiteForm.value.alerte,
      groupe_name: this.selectedGroupName
    };
    console.log(this.groups)
    console.log(website)
    this.apiService.post('/websites/', website).subscribe(
      response => {
        // Handle success
        this.snackBar.open("Le Website a été créée avec succès", "Fermer", { duration: 3000 });
        this.dialogRef.close();
        console.log(response);
      },      
      error => {
        console.error(error);
        // Handle error
      }
    );
  }

  openGroupeWebsiteDialog() {
    this.apiService.getAllGroupesWebsite().subscribe(
      response => {
        this.groups = response.results;
        console.log(this.groups)
        const dialogRef = this.dialog.open(GroupeWebsiteDialogComponent, {
          width: '450px',
          data: { groups: this.groups }
        });

        dialogRef.afterClosed().subscribe(result => {
          if (result) {
            // User chose a group or created a new one
            // You can now add the group to the website object
            this.websiteForm.patchValue({ groupe: result });
            this.selectedGroupName = result.name;
          }
        });
      },
      error => {
        console.error('Error fetching groups', error);
      }
    );
  }
}