import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoSecondTaskComponent } from './info-second-task.component';

describe('InfoSecondTaskComponent', () => {
  let component: InfoSecondTaskComponent;
  let fixture: ComponentFixture<InfoSecondTaskComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InfoSecondTaskComponent],
    });
    fixture = TestBed.createComponent(InfoSecondTaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
