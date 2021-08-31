# English-to-Clips programming language translator


## TODO:

- [ ] Create syntactic constructions, which are similar to correct English speech and are
equivalent to:
    
    - [x] deftemplate: 
    
    ```
    Cat template has properties of color, age, and name.
    (deftemplate cat
        (slot color) (slot age) (slot name))
    ```
    
    - [ ] defrule:
    
    ```
    If there exists cat named Bob then there exists a cat named Tom.
    (defrule rule1
        (cat (name “Bob”)) => (assert (cat (name “Tom”))))
    ```

    - [ ] assert:
    ```
    There exists a cat with the name Bob.
    (assert (cat (name “Bob”)))
    ```