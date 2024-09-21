import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-client-dialog',
  templateUrl: './client-dialog.component.html',
  styleUrls: ['./client-dialog.component.scss']
})
export class ClientDialogComponent {
  clientForm: FormGroup;
  compagnies: any[];

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<ClientDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private apiService: ApiService)
    {
      this.compagnies = data.compagnies;
      this.clientForm = this.fb.group({
      typeClient: ['', Validators.required],
      compagnie: ['', Validators.required],
    });
  }

  onSubmit() {
    const poste = {
      os: this.clientForm.value.typeClient,
      compagnie_id: this.clientForm.value.compagnie,
    };
    console.log(poste)
    this.apiService.addPoste(poste).subscribe(
      response => {
        console.log(response);

        // // Créer un lien pour télécharger le fichier texte
        // const blob = new Blob([response], { type: 'text/plain' });
        // const url = window.URL.createObjectURL(blob);
        // const a = document.createElement('a');
        // a.style.display = 'none';
        // a.href = url;
        // a.download = 'agent_info.txt';
        // document.body.appendChild(a);
        // a.click();
        // window.URL.revokeObjectURL(url);
        
        this.dialogRef.close();
      },
      error => {
        console.error(error);
      }
    );
  }
}
