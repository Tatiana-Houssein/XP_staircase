import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { NgOptimizedImage } from '@angular/common';
import { ExperimentComponent } from './experiments/experiment/experiment.component';
import { TacheInterferenteComponent } from './forms/tache-interferente/tache-interferente.component';
import { StoreModule } from '@ngrx/store';
import { appReducer } from './@store/reducers';
import { DespairComponent } from './header/despair/despair.component';
import { AppEffects } from './@store/effects';
import { EffectsModule } from '@ngrx/effects';
import { UserInfoComponent } from './forms/user-info/user-info.component';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    ExperimentComponent,
    TacheInterferenteComponent,
    DespairComponent,
    UserInfoComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgOptimizedImage,
    StoreModule.forRoot(
      { app: appReducer },
      {}
    ), // 'app' is the key for your reducer
    EffectsModule.forRoot([AppEffects]),
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
