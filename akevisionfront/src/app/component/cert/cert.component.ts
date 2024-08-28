import {Component} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import { GroupeWebsiteDialogComponent } from '../groupewebsite-dialog/groupewebsite-dialog.component';
import {WebsiteDialogComponent} from '../website-dialog/website-dialog.component';
import { CompagnieService } from '../../services/compagnie.service';

@Component({
  selector: 'app-cert',
  templateUrl: './cert.component.html',
  styleUrls: ['./cert.component.scss']
})
export class CertComponent {

  websiteMessage = '';
  groupewebsiteMessage ='';

  constructor(private dialog: MatDialog,
    private compagnieService: CompagnieService,
    ) {}

    openWebSiteDialog(): void {
    const dialogWebsiteRef = this.dialog.open(WebsiteDialogComponent, {
      width: '400px',
      
    });

    dialogWebsiteRef.afterClosed().subscribe(result => {
      if (result) {
        this.websiteMessage = "La compagnie a été créée avec succès";
      }
    });
  }

  openGroupeWebsiteDialog(): void {
    const dialogGroupeWebsiteRef = this.dialog.open(GroupeWebsiteDialogComponent, {
      width: '350px',
      height :'220px'
      
    });

    dialogGroupeWebsiteRef.afterClosed().subscribe(result => {
      if (result) {
        this.groupewebsiteMessage = "La compagnie a été créée avec succès";
      }
    });
  }
}
