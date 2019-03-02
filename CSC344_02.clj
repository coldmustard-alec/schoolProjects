(:require [clojure.core.matrix.operators :as M]) 
(:use clojure.core.matrix)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


(defn bind-values [m l]
  (map (fn [i]
    (cond 
      (seq? i) (bind-values m i)
      (vector? i) (vec (bind-values m i))
      :default (m i i)))
 l)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;RULES:
;;(* 1 x) => x
;;(* x 1) => x
;;(* 0 x) => 0
;;(* x 0) => 0
;;(+ 0 x) => x
;;(+ x 0) => x
;;(- (- x)) => x


(defn list-of-numbers? [l]
  (every? true?
    (map (fn [i]
      (if (seq? i)
          (list-of-numbers? i)
          (number? i)
        
      )
      ) 
   (rest l))
  )
)

(defn math-police [l]
  (if (list-of-numbers? l)
    (eval l)
    (let [op (first l) n1 (second l) n2 (last l)]
      (cond
        ;;"*"
        (and (= op '*) (= n1 '1)) n2
        (and (= op '*) (= n2 '1)) n1
        (and (= op '*) (= n1 '0)) 0
        (and (= op '*) (= n2 '0)) 0
        ;;"+"
        (and (= op '+) (= n1 '0)) n2
        (and (= op '+) (= n2 '0)) n1
        ;;"- -"
        (and (= op '-) (= (first n1) '-)) (second n2)
        :default l
      )
    )
  )
)


(defn simplify [l]
  (let [l1 (first l) l2 (second l)]
  (let [n1 (second l1) n2 (nth l1 2)
        n3 (second l2) n4 (nth l2 2)]
  (let [side1 (list '+ (math-police n1) (math-police n2))
        side2 (list '+ (math-police n3) (math-police n4))]
    (vector (math-police side1) (math-police side2))
  )
  )
  )
)


(defn top-secret [l]
  (let [t (first l) nums (second l) vars (nth l 2)
        n1 (first nums) n2 (second nums)
        v1 (first vars) v2 (second vars)]

  (simplify
    (vector
      (list '+ (list '* (first n1) v1) (list '* (first n2) v1))
      (list '+ (list '* (second n1) v2) (list '* (second n2) v2))
    )
  )
  )
)

(defn transform [l]
  (if (= (first (nth l 2)) 'transform)
    (top-secret (list 'transform (second l)
      (top-secret (list 'transform (second (nth l 2))
        (top-secret (nth (nth l 2) 2))))))
    (top-secret l)
  )
)


(defn evalexp [exp bindings]
  (transform (bind-values bindings exp)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


