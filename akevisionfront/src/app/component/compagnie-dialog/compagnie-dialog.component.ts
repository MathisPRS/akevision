import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { CompagnieService } from '../../services/compagnie.service';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-compagnie-dialog',
  templateUrl: './compagnie-dialog.component.html',
  styleUrls: ['./compagnie-dialog.component.scss']
})
export class CompagnieDialogComponent {
  compagnieForm = new FormGroup({
    nameCompagnie: new FormControl('', [Validators.required])
  });

  compagnieMessage = '';

  constructor(
    private compagnieService: CompagnieService,
    public dialogRef: MatDialogRef<CompagnieDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private snackBar: MatSnackBar
  ) {}

  onSubmit() {
    const name = this.compagnieForm.get('nameCompagnie').value;
    this.compagnieService.createCompagnie(name).subscribe(
      response => {
        this.snackBar.open("La compagnie a été créée avec succès", "Fermer", { duration: 3000 });
        this.dialogRef.close();
      },
      error => {
        if (error.error && error.error.name) {
          this.compagnieForm.get('nameCompagnie').setErrors({ 'compagnieExistante': true });
          this.compagnieMessage = error.error.name[0];
        } else {
          this.compagnieForm.get('nameCompagnie').setErrors({ 'unknownError': true });
          this.compagnieMessage = 'Une erreur s\'est produite. Veuillez réessayer.';
        }
      }
    );
  }
}
