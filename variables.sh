#!/bash/bin
# condiciones





nombre1=""
nombre2=""




read -p "introduzca el primer nombre:  " nombre1
read -p "introduzca el segundo nombre: " nombre2



if (( $nombre1 == $nombre2 )); then 
	echo "los nombres son iguales $nombre1 y $nombre2 "

else
	echo "los nombre son diferentes"

fi


