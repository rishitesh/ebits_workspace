import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EbitsTreasureComponent } from './ebits-treasure.component';

describe('EbitsTreasureComponent', () => {
  let component: EbitsTreasureComponent;
  let fixture: ComponentFixture<EbitsTreasureComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EbitsTreasureComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EbitsTreasureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
