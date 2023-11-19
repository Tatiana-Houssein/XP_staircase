js_script = """
    <script>
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'L').classList.add('bbutton-left');
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'R').classList.add('bbutton-right');


    const doc = window.parent.document;
    buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));
    const left_button = buttons.find(el => el.innerText === 'LEFT');
    const right_button = buttons.find(el => el.innerText === 'RIGHT');

    const left_button2 = buttons.find(el => el.innerText === 'L');
    const right_button2 = buttons.find(el => el.innerText === 'R');


    doc.addEventListener('keydown', function(e) {
    switch (e.keyCode) {
        case 37: // (37 = left arrow)
            left_button.click();
            break;
        case 39: // (39 = right arrow)
            right_button.click();
            break;
    }
    });


    left_button.addEventListener("click",function() {
    console.log("left")
    });

    right_button.addEventListener("click",function() {
    console.log("right")
    });

    left_button2.addEventListener("click",function() {
    console.log("left")
    });

    right_button2.addEventListener("click",function() {
    console.log("right")
    });

    </script>
    """  # noqa: E501

js_script_optimized = """<script>
const doc = window.parent.document;
const buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));

function addButtonClass(button, className) {
  button.classList.add(className);
}



const buttonMapping = {
  'L': 'bbutton-left',
  'R': 'bbutton-right',
  'LEFT': 'left_button',
  'RIGHT': 'right_button',
};

const buttonRefs = {};

buttons.forEach((button) => {
  const className = buttonMapping[button.innerText];
  if (className) {
    addButtonClass(button, className);
    buttonRefs[className] = button;
  }
});

doc.addEventListener('keydown', (e) => {
  const keyCodeMapping = {
    37: buttonRefs.left_button,
    39: buttonRefs.right_button,
  };

  const button = keyCodeMapping[e.keyCode];
  if (button) {
    button.click();
    scrollPlayerIntoView();
  }
});

Object.values(buttonRefs).forEach((button) => {
  button.addEventListener('click', () => {
    scrollPlayerIntoView();
    console.log(button.innerText.toLowerCase());
  });
});
</script>"""
