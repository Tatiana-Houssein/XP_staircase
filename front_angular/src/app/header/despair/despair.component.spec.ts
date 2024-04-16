import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DespairComponent } from './despair.component';

describe('DespairComponent', () => {
  let component: DespairComponent;
  let fixture: ComponentFixture<DespairComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DespairComponent]
    });
    fixture = TestBed.createComponent(DespairComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
