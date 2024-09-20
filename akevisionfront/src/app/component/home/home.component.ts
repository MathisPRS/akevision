import {Component} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {CompagnieDialogComponent} from '../compagnie-dialog/compagnie-dialog.component';
import { ClientDialogComponent } from '../client-dialog/client-dialog.component';
import { ApiService } from '../../services/api.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  compagnieMessage = '';

  constructor(private dialog: MatDialog,
    private apiService: ApiService,
    ) {}

  openCompagnieDialog(): void {
    const dialogCompagnieRef = this.dialog.open(CompagnieDialogComponent, {
      width: '350px',
      height :'220px'
      
    });

    dialogCompagnieRef.afterClosed().subscribe(result => {
      if (result) {
        this.compagnieMessage = "La compagnie a été créée avec succès";
      }
    });
  }

  openAgentDialog() {
    this.apiService.getAllCompagnies().subscribe(compagnies => {
      const dialogAgentRef = this.dialog.open(ClientDialogComponent, {
        width: '400px',
        data: { compagnies: compagnies }
      });
      console.log(compagnies)
      dialogAgentRef.afterClosed().subscribe(result => {
        if (result) {
          this.compagnieMessage = "La compagnie a été créée avec succès";
        }
      });
    });
  }


}
