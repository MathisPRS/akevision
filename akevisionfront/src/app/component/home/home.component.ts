import {Component} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {CompagnieDialogComponent} from '../compagnie-dialog/compagnie-dialog.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  compagnieMessage = '';

  constructor(private dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(CompagnieDialogComponent, {
      width: '400px',
      height :'400px'
      
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.compagnieMessage = "La compagnie a été créée avec succès";
      }
    });
  }
}
