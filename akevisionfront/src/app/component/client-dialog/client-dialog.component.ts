import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ClientService } from '../../services/client.service';

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
    private clientService: ClientService)
    {
      this.compagnies = data.compagnies;
      this.clientForm = this.fb.group({
      nomClient: ['', Validators.required],
      typeClient: ['', Validators.required],
      compagnie: ['', Validators.required],
      ipv4: ['', Validators.required]
    });
  }

  onSubmit() {
    const client = {
      name: this.clientForm.value.nomClient,
      os: this.clientForm.value.typeClient,
      compagnie_id: this.clientForm.value.compagnie,
      ipv4: this.clientForm.value.ipv4
    };
    this.clientService.createClient(client).subscribe(
      response => {
        console.log(response);
        this.clientService.getScriptClient(response.id).subscribe(
          response2 => {
            console.log(response2);
            this.clientService.downloadFile(response2, `client_${response.id}.zip`);
          }
        );
        
        this.dialogRef.close();
      },
      error => {
        console.error(error);
      }
    );
  }
}
