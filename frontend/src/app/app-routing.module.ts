import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './gate/gate.component';
import { HomeComponent } from './home/home.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { CreatePostComponent } from './create-post/create-post.component';


const routes: Routes = [
  HomeComponent.Route,
  ProfileEditorComponent.Route,
  GateComponent.Route,
  { path: 'admin', title: 'Admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
  { path: 'create', component: CreatePostComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule],
  providers: [AppTitleStrategy.Provider]
})
export class AppRoutingModule {}