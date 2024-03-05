import {User} from './user';
export class UserAuth {
  user: User;
  token: string;
  deleting: boolean;

  /**
   * Constructeur
   */
  constructor(user?: User, token?: string) {
    this.user = user;
    this.token = token;
    this.deleting = false;
  }

  /**
   * création de l'objet UserAuth à partir d'un userAuth en json
   * @param userAuth : json à sérialisé
   */
  static fromJSON(userAuth: any): UserAuth {
    if (userAuth) {
      userAuth.user = User.fromJSON(userAuth.user);
      return Object.assign(new UserAuth(), userAuth);
    }
    return null;
  }

  /**
   * création de l'objet UserAuth à partir de la string json d'un UserAuth
   * @param userAuthStr : string json d'un UserAuth
   */
  static parseJSON(userAuthStr: string): UserAuth {
    if (userAuthStr) {
      const userAuth = JSON.parse(userAuthStr);
      return this.fromJSON(userAuth);
    }
    return null;
  }

  /**
   * création de la string JSON d'un objet UserAuth
   * @param UserAuth : UserAuth à sérialisé en Json
   */
  static toJSON(userAuth: any): string {
    if (userAuth) {
        return JSON.stringify(Object.assign(new UserAuth(), userAuth));
    }
    return null;
  }

  /**
   * test si l'utilisateur appartient au groupe dont l'id est passé en paramètre
   * @param groupId : id de groupe
   */
  public isUserAuthInGroup(groupId: number) {
    return this.user && this.user.isUserInGroup(groupId);
  }

  public isDeleting(): boolean {
    return this.deleting;
  }

  public setDeleting(deleting: boolean) {
    this.deleting = deleting;
  }

}
