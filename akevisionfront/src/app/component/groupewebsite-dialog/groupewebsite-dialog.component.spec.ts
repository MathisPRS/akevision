import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupewebsiteDialogComponent } from './groupewebsite-dialog.component';

describe('GroupewebsiteDialogComponent', () => {
  let component: GroupewebsiteDialogComponent;
  let fixture: ComponentFixture<GroupewebsiteDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GroupewebsiteDialogComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GroupewebsiteDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
