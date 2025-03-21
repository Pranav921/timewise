function FriendsList() {
  return (
    <div className="flex flex-col">
      <p className="opacity-65 text-sm pl-4 py-2 select-none">Friends</p>
      <div className="hover:cursor-pointer">
        <FriendsListItem name="Gabriel" />
        <FriendsListItem name="Rohun" />
        <FriendsListItem name="Pranav" />
      </div>
    </div>
  );
}

type FriendsListItemProps = {
  name: string;
};

function FriendsListItem({ name }: FriendsListItemProps) {
  return (
    <div className="w-full block pl-4 py-2 hover:bg-gray-100">
      <p>{name}</p>
    </div>
  );
}

export default FriendsList;
