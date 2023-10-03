import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {AuthenticateComponent} from "./authenticate/authenticate.component";
import {RegisterComponent} from "./register/register.component";
import {AdminComponent} from "./admin/admin.component";
import {AdminGuard} from "./admin/admin.guard";
import {DemoUserComponent} from "./demo-user/demo-user.component";
import {DemoUserGuard} from "./demo-user/demo-user.guard";
import {RegularUserGuard} from "./regular-user/regular-user.guard";
import {RegularUserSearchComponent} from "./regular-user/regular-user-search/regular-user-search.component";
import {RegularUserHistoryComponent} from "./regular-user/regular-user-history/regular-user-history.component";
import {RegularUserRecommendationComponent} from "./regular-user/regular-user-recommendation/regular-user-recommendation.component";

const routes: Routes = [
  {
    path: 'authenticate',
    component: AuthenticateComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [
      AdminGuard
    ]
  },
  {
    path: 'demo-user',
    component: DemoUserComponent,
    canActivate: [
      DemoUserGuard
    ]
  },
  {
    path: 'regular-user',
    canActivate: [
      RegularUserGuard
    ],
    children: [
      {
        path: '',
        redirectTo: 'search',
        pathMatch: 'full'
      },
      {
        path: 'search',
        component: RegularUserSearchComponent
      },
      {
        path: 'history',
        component: RegularUserHistoryComponent
      },
      {
        path: 'recommendation/:id',
        component: RegularUserRecommendationComponent
      }
    ]
  },
  {
    path: '',
    redirectTo: 'authenticate',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
  static getRouteForRole(role: string | null): string {
    switch (role) {
      case "ADMIN":
        return '/admin'
      case "DEMO_USER":
        return '/demo-user'
      case "REGULAR_USER":
        return '/regular-user'
      default:
        return '/'
    }
  }
}
