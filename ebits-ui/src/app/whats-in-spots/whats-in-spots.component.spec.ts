import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WhatsInSpotsComponent } from './whats-in-spots.component';

describe('WhatsInSpotsComponent', () => {
  let component: WhatsInSpotsComponent;
  let fixture: ComponentFixture<WhatsInSpotsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WhatsInSpotsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WhatsInSpotsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
