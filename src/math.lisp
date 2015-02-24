;; math stuff

(define = (lambda (x y . z)
    (cond ((null? z) (__eq__ x y))
          ( (not (__eq__ x y)) #f )
          (else (= y (car z) (cdr z))))
    ))
(set-docstring = "(= a b ...) ==>   a == b == ...")

(from-py-load-as 'operator '(gt __gt__))
(define > (lambda (x y . z)
    (cond ((null? z) (__gt__ x y))
          ( (not (__gt__ x y)) #f )
          (else (> y (car z) (cdr z))))
    ))
(set-docstring > "(> a b ...) ==>   a > b > ...")

(from-py-load-as 'operator '(ge __ge__))
(define >= (lambda (x y . z)
    (cond ((null? z) (__ge__ x y))
          ( (not (__ge__ x y)) #f )
          (else (>= y (car z) (cdr z))))
    ))
(set-docstring >= "(>= a b ...) ==>   a >= b >= ...")

(from-py-load-as 'operator '(lt __lt__))
(define < (lambda (x y . z)
    (cond ((null? z) (__lt__ x y))
          ( (not (__lt__ x y)) #f )
          (else (< y (car z) (cdr z))))
    ))
(set-docstring < "(< a b ...) ==>   a < b < ...")

(from-py-load-as 'operator '(le __le__))
(define <= (lambda (x y . z)
    (cond ((null? z) (__le__ x y))
          ( (not (__le__ x y)) #f )
          (else (<= y (car z) (cdr z))))
    ))
(set-docstring <= "(<= a b ...) ==>   a <= b <= ...")

(from-py-load 'operator 'abs)

(from-py-load-as 'operator '(add __add__))  ;; __name will not show using help...
(define + (lambda (x y . z)
    (cond ((null? z) (__add__ x y))
          (else (+ (__add__ x y) (car z) (cdr z))))
    ))
(set-docstring + "(+ a b ...) ==>  a + b + ...")

(from-py-load-as 'operator '(mul __mul__))
(define * (lambda (x y . z)
    (cond ((null? z) (__mul__ x y))
          (else (* (__mul__ x y) (car z) (cdr z))))
    ))
(set-docstring * "(* a b ...) ==>  a * b * ...")

(from-py-load-as 'operator '(neg __neg__))
(define - (lambda (x . y)
    (cond ((null? y) (__neg__ x))
          ((null? (cdr y) )(+ x (__neg__ (car y))))
          (else (- (+ x (__neg__ (car y))) (cdr y) )))
    ))
(set-docstring - "(- x) ==> -x  OR (- a b ...) ==> a - b - ...")

(from-py-load-as 'operator '(truediv __truediv__))
(define / (lambda (x y) (__truediv__ x y)))
(set-docstring / "(/ x y) ==>  x / y  [floating point]")

(from-py-load-as 'operator '(floordiv __floordiv__))
(define // (lambda (x y) (__floordiv__ x y)))
(set-docstring // "(// x y) ==>  x // y  [floor division - int if both x and y are ints]")

