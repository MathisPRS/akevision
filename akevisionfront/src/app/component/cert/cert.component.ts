import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { GroupeWebsiteDialogComponent } from '../groupewebsite-dialog/groupewebsite-dialog.component';
import { WebsiteDialogComponent } from '../website-dialog/website-dialog.component';
import { WebsiteUpdateDialogComponent } from '../../website-update-dialog/website-update-dialog.component';

import { CompagnieService } from '../../services/compagnie.service';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-cert',
  templateUrl: './cert.component.html',
  styleUrls: ['./cert.component.scss']
})
export class CertComponent implements OnInit {
  websiteMessage = '';
  groupewebsiteMessage = '';
  websites: any[] = [];

  constructor(
    private dialog: MatDialog,
    private compagnieService: CompagnieService,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.loadWebsites();
  }

  loadWebsites(): void {
    this.apiService.getAllWebsite().subscribe(data => {
      this.websites = data;
      console.log(this.websites);
    });
  }

  openWebSiteDialog(): void {
    const dialogWebsiteRef = this.dialog.open(WebsiteDialogComponent, {
      width: '400px'
    });

    dialogWebsiteRef.afterClosed().subscribe(result => {
      if (result) {
        this.websiteMessage = "La compagnie a été créée avec succès";
        this.loadWebsites(); // Recharger les données après l'ajout
      }
    });
  }

  openGroupeWebsiteDialog(): void {
    const dialogGroupeWebsiteRef = this.dialog.open(GroupeWebsiteDialogComponent, {
      width: '350px',
      height: '220px'
    });

    dialogGroupeWebsiteRef.afterClosed().subscribe(result => {
      if (result) {
        this.groupewebsiteMessage = "La compagnie a été créée avec succès";
      }
    });
  }

  openUpdateDialog(website: any): void {
    const dialogRef = this.dialog.open(WebsiteUpdateDialogComponent, {
      width: '400px',
      data: { website: website }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadWebsites(); // Recharger les données après la mise à jour
      }
    });
  }
}
