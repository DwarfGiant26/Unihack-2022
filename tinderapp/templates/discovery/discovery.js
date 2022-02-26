let btn = document.querySelector('button');
let classObj = {
  ori: 'small',
  small: 'medium',
  medium: 'large',
  large: 'ori'
}

btn.addEventListener('click',()=>{
  btn.classList = classObj[btn.classList[0]];
});