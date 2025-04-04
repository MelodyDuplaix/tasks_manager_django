import { View, Text, TouchableOpacity, StyleSheet, Dimensions } from "react-native";
import { NavigationProp, useNavigation } from "@react-navigation/native";
import { useEffect } from "react";

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
    card: {
        backgroundColor: "#f9f9f9",
        padding: 15,
        borderRadius: 8,
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
        marginVertical: 10,
        alignItems: "center",
        alignSelf: "center",
        width: '100%',
    },
    text: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#333",
    },
});

export default function MenuItem({ name, link }: { name: string; link: string }) {
    const navigation = useNavigation<NavigationProp<ReactNavigation.RootParamList>>();

    return (
        <TouchableOpacity
            style={styles.card}
            onPress={() => navigation.navigate(link)}
        >
            <Text style={styles.text}>{name}</Text>
        </TouchableOpacity>
    );
}
