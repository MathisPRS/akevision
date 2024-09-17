import { Component, Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { WebsiteUpdateDialogComponent } from '../website-update-dialog/website-update-dialog.component';

@Component({
  selector: 'app-website-card',
  templateUrl: './website-card.component.html',
  styleUrls: ['./website-card.component.scss']
})
export class WebsiteCardComponent {
  @Input() website: any;

  constructor(private dialog: MatDialog) {}

  openUpdateDialog(): void {
    const dialogRef = this.dialog.open(WebsiteUpdateDialogComponent, {
      width: '400px',
      data: { website: this.website }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // Mettre à jour les données du site ici
        this.website = result;
      }
    });
  }
}
