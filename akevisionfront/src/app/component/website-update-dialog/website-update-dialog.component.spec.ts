import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebsiteUpdateDialogComponent } from './website-update-dialog.component';

describe('WebsiteUpdateDialogComponent', () => {
  let component: WebsiteUpdateDialogComponent;
  let fixture: ComponentFixture<WebsiteUpdateDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WebsiteUpdateDialogComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WebsiteUpdateDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
