import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TacheInterferenteComponent } from './tache-interferente.component';

describe('SecondPageComponent', () => {
  let component: TacheInterferenteComponent;
  let fixture: ComponentFixture<TacheInterferenteComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TacheInterferenteComponent]
    });
    fixture = TestBed.createComponent(TacheInterferenteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
