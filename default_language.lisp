(define #t __True__)
(define #f __False__)
(from-py-load-as 'operator '(not_ __not__))
(define not (lambda (x) (__not__ x)))
(set-docstring not "(not x) ==>   #t <--> #f")


(define else #t)
(define null '())
(from-py-load-as 'operator '(eq __eq__))
(define null? (lambda (x) (__eq__ x '())))
(set-docstring null? "(null? x) ==>  true x is the empty list '() ")


(define and (lambda (x . y)
    (cond ( (not x) #f)
        ((null? y) #t)
          (else (and (car y) (cdr y))))
    ))
(set-docstring and "(and arg1 arg2 ...) ==>  true if all args are true ")

(define or (lambda (x . y)
    (cond ( x #t)
        ((null? y) #f)
          (else (or (car y) (cdr y))))
    ))
(set-docstring or "(or arg1 arg2 ...) ==>  true if at least one arg is true ")

(define last (lambda (y) (cond ( (null? (cdr y)) (car y)) (else (last (cdr y))))))
(set-docstring last "(list a b ...) ==>  (a b ...) ")

(define append (lambda (x y)
    (cond ( (null? x) y)
        (else (cons (car x) (append (cdr x) y))))))
(define list (lambda (x . y) (append (cons x '()) y)))
(set-docstring list "(append '(a ...) '(b ...)) ==>  (a ... b ...) ")

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

;; the following does not work as expected since both "other" and
;; "if_true" would be evaluated
;(define if (lambda (test if_true other)
;    (cond (test if_true)
;          (else other))))
