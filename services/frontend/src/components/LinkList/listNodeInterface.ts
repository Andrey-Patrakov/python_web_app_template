export default interface ListNodeInteface {
	icon?: string,
	title: string,
	link?: string,
	click?: () => void,
	children?: ListNodeInteface[],
};
