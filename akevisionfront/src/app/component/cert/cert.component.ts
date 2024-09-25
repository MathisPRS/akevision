import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { GroupeWebsiteDialogComponent } from '../groupewebsite-dialog/groupewebsite-dialog.component';
import { WebsiteDialogComponent } from '../website-dialog/website-dialog.component';
import { WebsiteUpdateDialogComponent } from '../website-update-dialog/website-update-dialog.component';
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
  groupedWebsites: any[] = [];
  sortByGroup = true;

  constructor(
    private dialog: MatDialog,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.loadWebsites();
  }

  loadWebsites(): void {
    this.apiService.getAllWebsite().subscribe(data => {
      this.websites = data;
      this.updateGroupedWebsites();
    });
  }

  updateGroupedWebsites(): void {
    if (this.sortByGroup) {
      this.groupWebsitesByGroup();
    } else {
      this.groupWebsitesByColor();
    }
  }

  groupWebsitesByGroup(): void {
    const groups = [...new Set(this.websites.map(website => website.group))];
    this.groupedWebsites = groups.map(group => ({
      group,
      websites: this.websites.filter(website => website.group === group),
      isExpanded: false
    })).filter(group => group.websites.length > 0);
  }

  groupWebsitesByColor(): void {
    const colors = ['gris', 'rouge', 'orange', 'vert'];
    this.groupedWebsites = colors.map(color => ({
      color,
      websites: this.websites.filter(website => website.couleur === color),
      isExpanded: false
    })).filter(colorGroup => colorGroup.websites.length > 0);
  }

  toggleSortByGroup(): void {
    this.sortByGroup = true;
    this.updateGroupedWebsites();
  }

  toggleSortByColor(): void {
    this.sortByGroup = false;
    this.updateGroupedWebsites();
  }

  toggleExpand(group: any): void {
    group.isExpanded = !group.isExpanded;
  }

  openWebSiteDialog(): void {
    const dialogWebsiteRef = this.dialog.open(WebsiteDialogComponent, {
      width: '400px'
    });

    dialogWebsiteRef.afterClosed().subscribe(result => {
      if (result) {
        this.websiteMessage = "Le site a été créé avec succès";
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
        this.groupewebsiteMessage = "Le groupe a été créé avec succès";
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
