import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestMatMaterialComponent } from './test-mat-material.component';

describe('TestMatMaterialComponent', () => {
  let component: TestMatMaterialComponent;
  let fixture: ComponentFixture<TestMatMaterialComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestMatMaterialComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TestMatMaterialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
