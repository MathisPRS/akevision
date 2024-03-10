import {Component} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {CompagnieDialogComponent} from '../compagnie-dialog/compagnie-dialog.component';
import { ClientDialogComponent } from '../client-dialog/client-dialog.component';
import { CompagnieService } from '../../services/compagnie.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  compagnieMessage = '';

  constructor(private dialog: MatDialog,
    private compagnieService: CompagnieService,
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

  openClientDialog() {
    this.compagnieService.getAllCompagnies().subscribe(compagnies => {
      const dialogClientRef = this.dialog.open(ClientDialogComponent, {
        width: '400px',
        data: { compagnies: compagnies }
      });
      
      dialogClientRef.afterClosed().subscribe(result => {
        if (result) {
          this.compagnieMessage = "La compagnie a été créée avec succès";
        }
      });
    });
  }


}
