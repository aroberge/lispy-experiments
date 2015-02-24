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

(load 'math.lisp')


;; the following does not work as expected since both "other" and
;; "if_true" would be evaluated
;(define if (lambda (test if_true other)
;    (cond (test if_true)
;          (else other))))
