import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WhatsUpcomingComponent } from './whats-upcoming.component';

describe('WhatsUpcomingComponent', () => {
  let component: WhatsUpcomingComponent;
  let fixture: ComponentFixture<WhatsUpcomingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WhatsUpcomingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WhatsUpcomingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
