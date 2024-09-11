import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-website-card',
  templateUrl: './website-card.component.html',
  styleUrls: ['./website-card.component.scss']
})
export class WebsiteCardComponent {
  @Input() website: any;

}
