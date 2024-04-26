import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoThirdTaskComponent } from './info-third-task.component';

describe('InfoThirdTaskComponent', () => {
  let component: InfoThirdTaskComponent;
  let fixture: ComponentFixture<InfoThirdTaskComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InfoThirdTaskComponent]
    });
    fixture = TestBed.createComponent(InfoThirdTaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
