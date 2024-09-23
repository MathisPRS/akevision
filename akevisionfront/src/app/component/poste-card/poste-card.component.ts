// poste-card.component.ts
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-poste-card',
  templateUrl: './poste-card.component.html',
  styleUrls: ['./poste-card.component.scss']
})
export class PosteCardComponent {
  @Input() poste: any;
}
