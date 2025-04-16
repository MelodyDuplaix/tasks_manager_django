import {View, Text} from "react-native";
import React from "react";

export default function ProgressBar({ current, total }: { current: number, total: number }) {
    const percentage = Math.round((current / total) * 100)
    
    return (
        <View style={{ marginVertical: 10 }}>
            <Text style={{ alignSelf: "center", fontWeight: "bold"}}>Progression quotidienne</Text>
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 5 }}>
                <Text>{current} / {total}</Text>
                <Text>{percentage}%</Text>
            </View>
            <View style={{ height: 10, backgroundColor: '#E0E0E0', borderRadius: 5 }}>
                <View 
                    style={{
                        width: `${percentage}%`,
                        maxWidth: '100%',
                        height: '100%',
                        backgroundColor: '#4CAF50',
                        borderRadius: 5
                    }}
                />
            </View>
        </View>
    )
}