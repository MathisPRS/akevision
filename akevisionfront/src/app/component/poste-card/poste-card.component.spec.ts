import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PosteCardComponent } from './poste-card.component';

describe('PosteCardComponent', () => {
  let component: PosteCardComponent;
  let fixture: ComponentFixture<PosteCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PosteCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PosteCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
