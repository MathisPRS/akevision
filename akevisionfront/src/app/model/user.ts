import {Group} from './group';

export class User {
  id: number;
  username: string;
  password: string;
  firstName: string;
  lastName: string;
  groups: number[];

  /**
   * Constructeur
   */
  constructor(id?: number, username?: string, password?: string, firstName?: string, lastName?: string, groups?: number[]) {
    this.id = id;
    this.username = username;
    this.password = password;
    this.firstName = firstName;
    this.lastName = lastName;
    this.groups = groups;

  }

  /**
   * création de l'objet User à partir d'un user en json
   * @param userJson : json à sérialisé
   */
  static fromJSON(userJson: any): User {
    return Object.assign(new User(), userJson);
  }

  /**
   * test si l'utilisateur appartient au groupe dont l'id est passé en paramètre
   * @param groupId : id de groupe
   */
  public isUserInGroup(groupId: number) {
    for (const groupIdItem of this.groups) {
      if (groupIdItem === groupId) {
        return true;
      }
    }
    return false;
  }
}
