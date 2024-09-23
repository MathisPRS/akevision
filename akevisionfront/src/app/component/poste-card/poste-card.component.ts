import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-poste-card',
  templateUrl: './poste-card.component.html',
  styleUrls: ['./poste-card.component.scss']
})
export class PosteCardComponent implements OnInit {
  @Input() poste: any;
  timeDifference: string = '';

  ngOnInit(): void {
    this.calculateTimeDifference();
  }

  calculateTimeDifference(): void {
    const lastCommunication = new Date(this.poste.last_communication);
    const now = new Date();
    const diffInMs = now.getTime() - lastCommunication.getTime();
    const diffInSeconds = Math.floor(diffInMs / 1000);
    const diffInMinutes = Math.floor(diffInSeconds / 60);
    const diffInHours = Math.floor(diffInMinutes / 60);
    const diffInDays = Math.floor(diffInHours / 24);

    if (diffInDays > 0) {
      this.timeDifference = `${diffInDays} jours et ${diffInHours % 24} heures`;
    } else if (diffInHours > 0) {
      this.timeDifference = `${diffInHours} heures et ${diffInMinutes % 60} minutes`;
    } else if (diffInMinutes > 0) {
      this.timeDifference = `${diffInMinutes} minutes et ${diffInSeconds % 60} secondes`;
    } else {
      this.timeDifference = `${diffInSeconds} secondes`;
    }
  }

  getConnectionIndicatorColor(): string {
    return this.poste.is_connected ? 'green' : 'grey';
  }
}
