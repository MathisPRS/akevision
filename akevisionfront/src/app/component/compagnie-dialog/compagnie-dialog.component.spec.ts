import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompagnieDialogComponent } from './compagnie-dialog.component';

describe('CompagnieDialogComponent', () => {
  let component: CompagnieDialogComponent;
  let fixture: ComponentFixture<CompagnieDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CompagnieDialogComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CompagnieDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
